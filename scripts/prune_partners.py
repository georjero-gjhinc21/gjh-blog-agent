#!/usr/bin/env python3
"""Prune partner catalog entries that are out of contract or dead.

Compares every entry in the frontend partner catalog against the live
PartnerStack + Impact.com accounts (contract check) and re-validates each
outbound URL over HTTP (liveness check), then removes entries that:

  - have NO live contract (URL matches no active partnership/campaign), or
  - are DEAD (HTTP 404 at final URL, DNS failure, TLS failure, timeout).

Deliberately NOT pruned (kept with a warning instead):

  - 403/429 bot-blocked pages where the affiliate redirect demonstrably
    lands on the real vendor site (works for human visitors),
  - slow targets that time out for bots but resolve (flaky, for recheck),
  - anything on revenue grounds (payout/attribution data lives in the
    network dashboards; this script reports reachability only).

Fail-safes (never mass-delete on an outage):

  - a control URL must be reachable, otherwise nothing is pruned;
  - if either network API errors or returns an empty program list, the
    no-contract rule is disabled for that run (liveness still applies);
  - default mode is --dry-run (report only); --apply writes files.

Usage:
  venv/bin/python scripts/prune_partners.py                      # dry run
  venv/bin/python scripts/prune_partners.py --apply              # prune files
  venv/bin/python scripts/prune_partners.py --apply --skip-live-check
  venv/bin/python scripts/prune_partners.py --report prune_report.md

Exit code is always 0 (CI-safe); read the report/stdout for results.
"""
from __future__ import annotations

import argparse
import concurrent.futures
import json
import re
import sys
import time
from pathlib import Path
from urllib.parse import urlparse

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/126.0 Safari/537.36"
)
CONTROL_URL = "https://www.google.com"

ENTRY_RE = re.compile(r"  \{\n(?:.*\n)*?  \},\n")
SLUG_RE = re.compile(r"slug:\s*'([^']+)'")
NAME_RE = re.compile(r"name:\s*'((?:[^'\\]|\\.)*)'")
URL_RE = re.compile(r"url:\s*'([^']+)'")
FEATURED_RE = re.compile(r"featured:\s*true")


def parse_ts(path: Path) -> tuple[str, list[dict]]:
    """Return (full_text, entries). Each entry keeps its raw block for removal."""
    src = path.read_text()
    entries = []
    for m in ENTRY_RE.finditer(src):
        block = m.group(0)
        slug = SLUG_RE.search(block)
        url = URL_RE.search(block)
        if not slug or not url:
            continue
        name = NAME_RE.search(block)
        entries.append({
            "slug": slug.group(1),
            "name": name.group(1) if name else slug.group(1),
            "url": url.group(1),
            "featured": bool(FEATURED_RE.search(block)),
            "block": block,
            "source": path.name,
        })
    return src, entries


def norm_url(u: str) -> str:
    return u.strip().rstrip("/")


def fetch_contracts() -> tuple[set[str], bool, dict]:
    """Return (live_affiliate_urls, verified, notes).

    verified is False if either network API errored or came back empty,
    in which case callers must NOT prune on no-contract grounds.
    """
    live: set[str] = set()
    notes: dict = {}
    verified = True
    try:
        from utils.partnerstack_client import PartnerStackClient
        progs = PartnerStackClient().get_all_programs() or []
        notes["partnerstack"] = f"{len(progs)} active partnerships"
        if not progs:
            verified = False
            notes["partnerstack"] += " (EMPTY -> contract check disabled)"
        for p in progs:
            if p.get("affiliate_url"):
                live.add(norm_url(p["affiliate_url"]))
    except Exception as e:  # noqa: BLE001 - fail-safe must never raise
        verified = False
        notes["partnerstack"] = f"API error, contract check disabled: {e}"
    try:
        from utils.impact_client import ImpactClient
        camps = ImpactClient().get_all_campaigns() or []
        notes["impact"] = f"{len(camps)} active campaigns"
        if not camps:
            verified = False
            notes["impact"] += " (EMPTY -> contract check disabled)"
        for c in camps:
            if c.get("affiliate_url"):
                live.add(norm_url(c["affiliate_url"]))
    except Exception as e:  # noqa: BLE001 - fail-safe must never raise
        verified = False
        notes["impact"] = f"API error, contract check disabled: {e}"
    return live, verified, notes


def check_url(url: str, timeout: int = 20) -> tuple[str, str]:
    """Return (verdict, detail). Verdicts: alive | dead | bot-blocked | flaky."""
    try:
        r = requests.get(url, headers={"User-Agent": UA},
                         allow_redirects=True, timeout=timeout)
    except requests.exceptions.SSLError as e:
        return "dead", f"TLS failure: {str(e)[:120]}"
    except requests.exceptions.ConnectionError as e:
        msg = str(e)
        if "NameResolutionError" in msg or "Name or service not known" in msg:
            return "dead", f"DNS failure: {msg[:120]}"
        if "Read timed out" in msg or "read timeout" in msg.lower():
            return "flaky", f"target timed out mid-redirect: {msg[:120]}"
        return "dead", f"connection error: {msg[:120]}"
    except (requests.exceptions.ConnectTimeout,
            requests.exceptions.ReadTimeout):
        return "flaky", "timeout"
    except Exception as e:  # noqa: BLE001
        return "flaky", f"{type(e).__name__}: {str(e)[:120]}"
    code = r.status_code
    if 200 <= code < 400:
        return "alive", f"HTTP {code} -> {r.url[:120]}"
    if code in (403, 429):
        # Affiliate redirect demonstrably working (lands on vendor page)
        # but vendor WAF rate-limits/bot-blocks us -> keep.
        if urlparse(r.url).netloc != urlparse(url).netloc:
            return "bot-blocked", f"HTTP {code} at vendor page {r.url[:120]}"
        return "bot-blocked", f"HTTP {code} without redirect; kept (unproven)"
    if code == 404:
        return "dead", f"HTTP 404 (final: {r.url[:120]})"
    return "flaky", f"HTTP {code} (final: {r.url[:120]})"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true",
                    help="write pruned files (default: dry run)")
    ap.add_argument("--skip-live-check", action="store_true",
                    help="contract check only, no HTTP validation")
    ap.add_argument("--timeout", type=int, default=20)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--report", default="prune_report.md")
    ap.add_argument("--data-ts", default="frontend/lib/partners-data.ts")
    ap.add_argument("--generated-ts", default="frontend/lib/partners-generated.ts")
    ap.add_argument("--catalog-json", default="data/program_categories.json")
    args = ap.parse_args()

    data_path = Path(args.data_ts)
    gen_path = Path(args.generated_ts)
    if not data_path.exists() or not gen_path.exists():
        print(f"Catalog files not found ({data_path}, {gen_path}); nothing to do.")
        return 0

    data_src, data_entries = parse_ts(data_path)
    gen_src, gen_entries = parse_ts(gen_path)
    entries = data_entries + gen_entries
    print(f"Catalog entries: {len(entries)} "
          f"({len(data_entries)} curated + {len(gen_entries)} generated)")

    # Fail-safe 1: control URL must be reachable.
    try:
        requests.get(CONTROL_URL, headers={"User-Agent": UA}, timeout=15)
    except Exception as e:  # noqa: BLE001
        print(f"ABORT: control URL unreachable ({e}); pruning disabled.")
        return 0

    # Contract check against live accounts.
    live_urls, contracts_verified, notes = fetch_contracts()
    print("Live contracts:", notes, "| verified:", contracts_verified)

    decisions: dict[str, tuple[str, str]] = {}  # slug -> (action, reason)
    need_http: list[dict] = []
    for e in entries:
        if contracts_verified and norm_url(e["url"]) not in live_urls:
            decisions[e["slug"]] = ("prune", "no-contract: URL matches no "
                                            "active PartnerStack/Impact program")
        elif not args.skip_live_check:
            need_http.append(e)
        else:
            decisions[e["slug"]] = ("keep", "in contract (live check skipped)")

    # Liveness check for the rest.
    if need_http:
        print(f"HTTP-checking {len(need_http)} in-contract URLs...")
        with concurrent.futures.ThreadPoolExecutor(
                max_workers=args.workers) as ex:
            futs = {ex.submit(check_url, e["url"], args.timeout): e
                    for e in need_http}
            for i, fut in enumerate(
                    concurrent.futures.as_completed(futs), 1):
                e = futs[fut]
                verdict, detail = fut.result()
                if verdict == "alive":
                    decisions[e["slug"]] = ("keep", detail)
                elif verdict == "dead":
                    decisions[e["slug"]] = ("prune", f"dead-link: {detail}")
                else:  # bot-blocked / flaky -> keep, report only
                    decisions[e["slug"]] = ("keep", f"{verdict}: {detail}")
                if i % 25 == 0:
                    print(f"  ...{i}/{len(need_http)}")
                time.sleep(0.2)

    by_slug = {e["slug"]: e for e in entries}
    pruned = [(s, r) for s, (a, r) in decisions.items() if a == "prune"]
    kept_warnings = [(s, r) for s, (a, r) in decisions.items()
                     if a == "keep" and (r.startswith("bot-blocked")
                                         or r.startswith("flaky"))]
    print(f"Result: {len(pruned)} to prune, "
          f"{len(kept_warnings)} kept-with-warning, "
          f"{len(entries) - len(pruned) - len(kept_warnings)} clean.")

    # Revenue signals: report-only, never a prune reason.
    revenue_note = "revenue attribution lives in the network dashboards; " \
                   "no auto-prune on revenue."
    try:
        from utils.impact_client import ImpactClient
        stats = ImpactClient().get_stats(days=30)
        if stats:
            revenue_note = f"Impact 30d stats snapshot: " \
                           f"{str(stats)[:300]} (report-only)"
    except Exception as e:  # noqa: BLE001
        revenue_note = f"Impact stats unavailable: {e} (report-only)"

    # Write report.
    lines = ["# Partner prune report", "",
             f"Catalog: {len(entries)} entries | "
             f"prune: {len(pruned)} | warnings: {len(kept_warnings)}",
             f"Contracts verified: {contracts_verified} ({notes})",
             f"Revenue: {revenue_note}", "",
             "## Pruned" if pruned else "## Pruned (none)"]
    for slug, reason in sorted(pruned):
        e = by_slug[slug]
        flag = " [FEATURED]" if e["featured"] else ""
        lines.append(f"- {slug} ({e['name']}){flag} [{e['source']}] "
                     f"{e['url']} -- {reason}")
    lines += ["", "## Kept with warning" if kept_warnings
              else "## Kept with warning (none)"]
    for slug, reason in sorted(kept_warnings):
        e = by_slug[slug]
        lines.append(f"- {slug} ({e['name']}) [{e['source']}] -- {reason}")
    Path(args.report).write_text("\n".join(lines) + "\n")
    print(f"Report written to {args.report}")

    if not pruned:
        return 0
    if not args.apply:
        print("Dry run: files unchanged. Re-run with --apply to prune.")
        return 0

    prune_slugs = {s for s, _ in pruned}
    pruned_urls = {by_slug[s]["url"] for s in prune_slugs}
    for path, src in ((data_path, data_src), (gen_path, gen_src)):
        out = src
        for e in entries:
            if e["source"] == path.name and e["slug"] in prune_slugs:
                out = out.replace(e["block"], "", 1)
        path.write_text(out)
        left = len(SLUG_RE.findall(out))
        print(f"Updated {path}: {left} entries remain.")

    # Keep the classifier JSON in sync so re-export cannot resurrect URLs.
    json_path = Path(args.catalog_json)
    if json_path.exists():
        data = json.loads(json_path.read_text())
        before = len(data)
        data = {k: v for k, v in data.items()
                if v.get("affiliate_url") not in pruned_urls}
        json_path.write_text(json.dumps(data, indent=2))
        print(f"Synced {json_path}: {before} -> {len(data)} programs.")
    else:
        print(f"{json_path} absent; skipped JSON sync.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
