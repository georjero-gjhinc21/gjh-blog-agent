#!/usr/bin/env python3
"""Verify that fixed affiliate links are now working."""
import requests
import re
from pathlib import Path

def test_link(url, use_get=True):
    """Test if a link is accessible."""
    try:
        if use_get:
            # Use GET for affiliate links (they may redirect)
            response = requests.get(url, allow_redirects=True, timeout=10)
        else:
            response = requests.head(url, allow_redirects=True, timeout=10)

        return {
            'url': url,
            'status': response.status_code,
            'final_url': response.url,
            'working': response.status_code < 400
        }
    except Exception as e:
        return {
            'url': url,
            'status': 'ERROR',
            'error': str(e),
            'working': False
        }

def extract_links_from_posts():
    """Extract all affiliate links from blog posts."""
    posts_dir = Path("frontend/posts")
    links = {}

    for post_file in posts_dir.glob("*.md"):
        content = post_file.read_text()

        # Find all affiliate links
        affiliate_links = re.findall(r'https://(?:partnerstack\.com|partner\.link|try\.web\.clickup\.com|get\.gusto\.com|try\.folk\.app|try\.goaura\.com)[^\s\)]+', content)

        if affiliate_links:
            links[post_file.name] = affiliate_links

    return links

def main():
    print("="*80)
    print("VERIFYING FIXED AFFILIATE LINKS")
    print("="*80)

    all_links = extract_links_from_posts()

    # Get unique links
    unique_links = set()
    for links in all_links.values():
        unique_links.update(links)

    print(f"\n📊 Found {len(unique_links)} unique affiliate links")

    # Categorize links
    partnerstack_links = [l for l in unique_links if 'partnerstack.com' not in l or 'try.' in l or 'get.' in l]
    partner_link_links = [l for l in unique_links if 'partner.link' in l]

    print(f"\n🧪 Testing PartnerStack links ({len(partnerstack_links)})...")
    ps_results = []
    for link in sorted(partnerstack_links):
        print(f"\n   Testing: {link[:70]}...")
        result = test_link(link, use_get=True)
        ps_results.append(result)
        status_emoji = "✅" if result['working'] else "❌"
        print(f"      {status_emoji} Status: {result.get('status', 'ERROR')}")

    print(f"\n🧪 Testing partner.link URLs ({len(partner_link_links)})...")
    pl_results = []
    for link in sorted(partner_link_links):
        print(f"\n   Testing: {link[:70]}...")
        result = test_link(link, use_get=True)
        pl_results.append(result)
        status_emoji = "✅" if result['working'] else "❌"
        print(f"      {status_emoji} Status: {result.get('status', 'ERROR')}")

    all_results = ps_results + pl_results

    print(f"\n" + "="*80)
    print(f"📋 SUMMARY:")
    working_count = sum(1 for r in all_results if r['working'])
    print(f"   Total links tested: {len(all_results)}")
    print(f"   Working links: {working_count}/{len(all_results)}")
    print(f"   Broken links: {len(all_results) - working_count}/{len(all_results)}")

    if working_count < len(all_results):
        print(f"\n❌ BROKEN LINKS:")
        for result in all_results:
            if not result['working']:
                print(f"   - {result['url']}")
                print(f"     Error: {result.get('error', result.get('status'))}")

    print("\n" + "="*80)

    return working_count == len(all_results)

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
