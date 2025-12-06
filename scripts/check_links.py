#!/usr/bin/env python3
"""Scan frontend/posts for URLs and report broken links to a file.
Exits 0 always; outputs to ./broken_links.txt
"""
import requests
from pathlib import Path
import re

posts = sorted(Path('frontend/posts').glob('*.md'))
url_to_files = {}
for p in posts:
    text = p.read_text()
    for m in re.findall(r"https?://[^)\]\'\"\s]+", text):
        u = m.strip().rstrip(')\'\"')
        url_to_files.setdefault(u, set()).add(str(p))

broken = []
for u, files in sorted(url_to_files.items()):
    try:
        r = requests.head(u, allow_redirects=True, timeout=10)
        code = r.status_code
    except Exception:
        code = 0
    if code == 0 or (code >= 400 and code < 600):
        broken.append((u, code, sorted(files)))

out = Path('broken_links.txt')
if broken:
    with out.open('w') as f:
        for u, code, files in broken:
            f.write(f"{code} {u} in files: {', '.join(files)}\n")
else:
    # ensure empty file
    out.write_text('')

print(f"Checked {len(url_to_files)} unique URLs. Broken: {len(broken)}")
