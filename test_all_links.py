#!/usr/bin/env python3
"""Test all affiliate links in blog posts."""
import requests
import re
from pathlib import Path

def extract_links_from_posts():
    """Extract all affiliate links from blog posts."""
    posts_dir = Path("frontend/posts")
    links = {}

    for post_file in posts_dir.glob("*.md"):
        content = post_file.read_text()

        # Find all affiliate links
        affiliate_links = re.findall(r'https://(?:partnerstack\.com|partner\.link)[^\s\)]+', content)

        if affiliate_links:
            links[post_file.name] = affiliate_links

    return links

def test_link(url):
    """Test if a link is accessible."""
    try:
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

def main():
    print("="*80)
    print("AFFILIATE LINK VERIFICATION REPORT")
    print("="*80)

    all_links = extract_links_from_posts()

    # Count stats
    total_posts = len(list(Path("frontend/posts").glob("*.md")))
    posts_with_links = len(all_links)
    total_link_instances = sum(len(links) for links in all_links.values())
    unique_links = set()
    for links in all_links.values():
        unique_links.update(links)

    print(f"\n📊 STATISTICS:")
    print(f"   Total blog posts: {total_posts}")
    print(f"   Posts with affiliate links: {posts_with_links}")
    print(f"   Posts WITHOUT affiliate links: {total_posts - posts_with_links}")
    print(f"   Total affiliate link instances: {total_link_instances}")
    print(f"   Unique affiliate links: {len(unique_links)}")

    print(f"\n🔗 UNIQUE LINKS FOUND:")
    for i, link in enumerate(sorted(unique_links), 1):
        print(f"   {i}. {link}")

    print(f"\n🧪 TESTING LINKS...")
    results = []
    for link in sorted(unique_links):
        print(f"   Testing: {link[:60]}...")
        result = test_link(link)
        results.append(result)
        status_emoji = "✅" if result['working'] else "❌"
        print(f"      {status_emoji} Status: {result.get('status', 'ERROR')}")

    print(f"\n📋 SUMMARY:")
    working_count = sum(1 for r in results if r['working'])
    print(f"   Working links: {working_count}/{len(results)}")
    print(f"   Broken links: {len(results) - working_count}/{len(results)}")

    if working_count < len(results):
        print(f"\n❌ BROKEN LINKS:")
        for result in results:
            if not result['working']:
                print(f"   - {result['url']}")
                print(f"     Error: {result.get('error', result.get('status'))}")

    print("\n" + "="*80)

    return working_count == len(results)

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
