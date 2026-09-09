#!/usr/bin/env python3
"""Classify affiliate programs into the canonical site taxonomy (Slice 2).

Reads programs from PartnerStack + Impact clients, asks local Ollama
(llama3.1:8b) to pick EXACTLY one bucket from the closed list, validates,
falls back to keyword rules, and writes reviewable JSON. Idempotent and
resumable: already-classified entries (by external_id or name) are skipped
unless --refresh is passed.

Usage:
  venv/bin/python utils/classify_programs.py --limit 3        # prompt validation
  venv/bin/python utils/classify_programs.py                  # full run (~90)
  venv/bin/python utils/classify_programs.py --refresh        # reclassify all

Output: data/program_categories.json
  { "<key>": {"name":..., "network":..., "category":..., "keywords":[...],
              "vendor_domain":..., "method":"llm|rules", "raw":...} }
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

BUCKETS = [
    "Project Management",
    "HR & Payroll",
    "Cybersecurity & Identity",
    "Communication & Collaboration",
    "Marketing & CRM",
    "Finance & Accounting",
    "IT & DevOps",
    "Data & Analytics",
    "Legal & Compliance",
    "Travel & Expense",
    "Operations",
    "Other",
]

# Deterministic fallback when the model output is unusable.
RULES = [
    (["payroll", "hr", "hiring", "benefits", "onboarding", "recruit"], "HR & Payroll"),
    (["sso", "mfa", "identity", "security", "vpn", "antivirus", "firewall", "compliance", "soc 2", "edr"], "Cybersecurity & Identity"),
    (["crm", "email marketing", "marketing", "sales", "lead"], "Marketing & CRM"),
    (["accounting", "invoice", "bookkeeping", "tax", "expense", "payroll"], "Finance & Accounting"),
    (["project", "task", "kanban", "gantt", "sprint"], "Project Management"),
    (["chat", "meeting", "video", "phone", "voip", "sms", "communication"], "Communication & Collaboration"),
    (["server", "cloud", "deploy", "devops", "monitor", "uptime", "hosting"], "IT & DevOps"),
    (["analytics", "dashboard", "bi ", "data", "insight"], "Data & Analytics"),
    (["legal", "contract", "esignature", "audit"], "Legal & Compliance"),
    (["travel", "booking", "flight", "hotel"], "Travel & Expense"),
]


def rule_classify(text: str) -> str:
    t = f" {text.lower()} "
    for keywords, bucket in RULES:
        if any(k in t for k in keywords):
            return bucket
    return "Other"


def vendor_domain(url: str) -> str:
    try:
        return urlparse(url).netloc.lower().removeprefix("www.")
    except Exception:
        return ""


def llm_classify(client, name: str, domain: str, keywords: list[str]) -> tuple[str, str]:
    prompt = (
        "Classify this business software product into EXACTLY ONE of these categories:\n"
        + "\n".join(f"- {b}" for b in BUCKETS)
        + f"\n\nProduct: {name}\nVendor domain: {domain or 'unknown'}\n"
        f"Keywords: {', '.join(keywords) or 'none'}\n\n"
        "Reply with ONLY the category name, nothing else."
    )
    try:
        out = client.generate(prompt, system="You are a precise software categorizer.", temperature=0.0).strip()
    except Exception as e:
        return "Other", f"llm-error: {e}"
    # Accept exact match or match after stripping quotes/punctuation.
    cleaned = out.strip("\"'*. ").strip()
    if cleaned in BUCKETS:
        return cleaned, out
    for b in BUCKETS:
        if cleaned.lower() == b.lower():
            return b, out
    return rule_classify(f"{name} {domain} {' '.join(keywords)}"), f"fallback, raw={out!r}"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--refresh", action="store_true")
    ap.add_argument("--out", default="data/program_categories.json")
    args = ap.parse_args()

    from utils.partnerstack_client import PartnerStackClient
    from utils.impact_client import ImpactClient
    from utils.ollama_client import OllamaClient

    programs = []
    for p in PartnerStackClient().get_all_programs():
        p["network"] = "partnerstack"
        programs.append(p)
    for p in ImpactClient().get_all_campaigns():
        p["network"] = p.get("network", "impact")
        programs.append(p)
    # Only classifiable rows: must have a usable outbound link.
    programs = [p for p in programs if p.get("affiliate_url")]
    if args.limit:
        programs = programs[: args.limit]
    print(f"Classifying {len(programs)} programs...")

    out_path = Path(args.out)
    existing: dict = {}
    if out_path.exists() and not args.refresh:
        existing = json.loads(out_path.read_text())

    client = OllamaClient()
    results = dict(existing)
    done = 0
    for p in programs:
        key = p.get("external_id") or p["name"]
        if key in results and not args.refresh:
            continue
        name = p.get("name", "Unknown")
        domain = vendor_domain(p.get("affiliate_url", "") or p.get("base_url", ""))
        kws = p.get("keywords") or []
        category, raw = llm_classify(client, name, domain, kws)
        if category == "Other" and "fallback" not in str(raw) and "llm-error" not in str(raw):
            method = "llm"
        elif "llm-error" in str(raw):
            method = "rules"
            category = rule_classify(f"{name} {domain} {' '.join(kws)}")
        else:
            method = "rules" if str(raw).startswith("fallback") else "llm"
        results[key] = {
            "name": name,
            "network": p.get("network"),
            "category": category,
            "keywords": kws,
            "vendor_domain": domain,
            "affiliate_url": p.get("affiliate_url"),
            "method": method,
            "raw": raw,
        }
        done += 1
        if done % 10 == 0:
            print(f"  ...{done}/{len(programs)}")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(results, indent=2))
    from collections import Counter
    print("Wrote", out_path)
    print(Counter(v["category"] for v in results.values()))
    print("Method split:", Counter(v["method"] for v in results.values()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
