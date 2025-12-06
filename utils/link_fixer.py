from pathlib import Path
import requests

LINK_FIXES = {
    "https://www.wati.io/pricing/": "https://affiliates.wati.io/mq5gz7zpyn9a",
    "https://partnerstack.com/go/gusto?ref=gjhblog": "https://get.gusto.com/703bagjmmd7u",
    # Add more mappings as discovered
}


def fix_links_in_post(post_path: str) -> int:
    p = Path(post_path)
    content = p.read_text()
    fixed = 0
    for broken, correct in LINK_FIXES.items():
        if broken in content:
            content = content.replace(broken, correct)
            fixed += 1
    if fixed:
        p.write_text(content)
    return fixed


def validate_links_in_post(post_path: str) -> list:
    """Return list of (url, status_code) for URLs that are broken (non-2xx)."""
    p = Path(post_path)
    content = p.read_text()
    urls = set()
    for part in content.split():
        if part.startswith('http://') or part.startswith('https://'):
            urls.add(part.strip().rstrip(')\'\"'))

    broken = []
    for u in urls:
        try:
            r = requests.head(u, allow_redirects=True, timeout=10)
            code = r.status_code
        except Exception:
            code = 0
        if code == 0 or code >= 400:
            broken.append((u, code))
    return broken
