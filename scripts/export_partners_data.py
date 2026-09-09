#!/usr/bin/env python3
"""Export classified affiliate programs to frontend partners-data.ts (Slice 4).

Reads data/program_categories.json (reviewed classifier output), preserves
hand-curated entries by slug, dedupes by vendor domain across networks,
drafts missing descriptions via the NVIDIA LLM (flagged in stdout, not in output),
and writes a TS data module.

Usage:
  venv/bin/python scripts/export_partners_data.py --preserve clickup,gusto,... --out data/partners-data.ts
  (then copy the output over frontend/lib/partners-data.ts in the main repo,
   build, and ship via the normal PR flow)
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

PLATFORM = {"partnerstack": "PartnerStack", "impact": "Impact"}


def slugify(name: str, taken: set[str]) -> str:
    base = re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", name.lower())).strip("-") or "partner"
    slug, i = base, 2
    while slug in taken:
        slug = f"{base}-{i}"
        i += 1
    taken.add(slug)
    return slug


def draft_description(client, name: str, domain: str, keywords: list[str], category: str) -> str:
    prompt = (
        f"Write ONE neutral factual sentence (max 25 words) describing what the business product "
        f"'{name}' ({domain or 'website unknown'}) does. Category context: {category}. "
        f"Keywords: {', '.join(keywords) or 'none'}. No hype, no call to action, no pricing claims."
    )
    try:
        out = client.generate(prompt, system="You write factual product descriptions.", temperature=0.2).strip()
        out = re.sub(r"\s+", " ", out).strip("\"' ")
        sentences = re.split(r"(?<=[.!?])\s+", out)
        return sentences[0][:220] if sentences else ""
    except Exception as e:
        print(f"  draft failed for {name}: {e}")
        return ""


def ts_escape(s: str) -> str:
    return s.replace("\\", "\\\\").replace("'", "\\'")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", default="data/program_categories.json")
    ap.add_argument("--out", default="data/partners-data.ts")
    ap.add_argument("--preserve", default="", help="comma-separated slugs to skip (hand-curated)")
    ap.add_argument("--draft-descriptions", action="store_true")
    args = ap.parse_args()

    data = json.loads(Path(args.input).read_text())
    preserve = {s.strip() for s in args.preserve.split(",") if s.strip()}

    # Dedupe by vendor domain across networks: prefer rows with real
    # descriptions, then PartnerStack, then first-seen.
    def quality(v):
        has_desc = bool((v.get("description") or "") and not v["description"].startswith("http"))
        return (has_desc, v.get("network") == "partnerstack")

    by_domain: dict[str, dict] = {}
    for key, v in data.items():
        if not v.get("affiliate_url"):
            continue
        dom = v.get("vendor_domain") or v["name"].lower()
        if dom not in by_domain or quality(v) > quality(by_domain[dom]):
            by_domain[dom] = v
    print(f"Unique vendor domains: {len(by_domain)}")

    client = None
    if args.draft_descriptions:
        from utils.nvidia_client import NvidiaClient
        client = NvidiaClient()

    taken = set(preserve)
    entries, skipped, drafted = [], 0, 0
    for v in sorted(by_domain.values(), key=lambda x: x["name"].lower()):
        name = v["name"]
        slug = slugify(name, taken)
        if slug in preserve or any(s == slug for s in preserve):
            skipped += 1
            continue
        desc = v.get("description") or ""
        if desc.startswith("http") or not desc:
            desc = ""
        if not desc and client:
            desc = draft_description(client, name, v.get("vendor_domain", ""), v.get("keywords", []), v.get("category", "Other"))
            if desc:
                drafted += 1
        if not desc:
            desc = f"{name} — partner program listed in the GJH Consulting partner catalog."
        excerpt = desc if len(desc) <= 140 else desc[:137].rsplit(" ", 1)[0] + "..."
        entries.append({
            "slug": slug,
            "name": name,
            "platform": PLATFORM.get(v.get("network", ""), "PartnerStack"),
            "category": v.get("category", "Other"),
            "description": desc,
            "excerpt": excerpt,
            "keywords": v.get("keywords", [])[:8],
            "url": v["affiliate_url"],
            "logo": "",
            "cta": f"Explore {name}",
        })

    lines = ["import type { PartnerProgram } from './partners'", "", "export const partnerProgramsData: PartnerProgram[] = ["]
    for e in entries:
        lines.append("  {")
        lines.append(f"    slug: '{ts_escape(e['slug'])}',")
        lines.append(f"    name: '{ts_escape(e['name'])}',")
        lines.append(f"    platform: '{e['platform']}',")
        lines.append(f"    category: '{ts_escape(e['category'])}',")
        lines.append(f"    description: '{ts_escape(e['description'])}',")
        lines.append(f"    excerpt: '{ts_escape(e['excerpt'])}',")
        kws = ", ".join(f"'{ts_escape(k)}'" for k in e["keywords"])
        lines.append(f"    keywords: [{kws}],")
        lines.append(f"    url: '{ts_escape(e['url'])}',")
        lines.append("    logo: '',")
        lines.append(f"    cta: '{ts_escape(e['cta'])}',")
        lines.append("  },")
    lines.append("];")
    lines.append("")
    Path(args.out).write_text("\n".join(lines))
    print(f"Wrote {args.out}: {len(entries)} new entries, {skipped} preserved-skipped, {drafted} descriptions drafted")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
