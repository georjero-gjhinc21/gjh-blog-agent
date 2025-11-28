#!/usr/bin/env python3
"""Fix broken affiliate links in blog posts with real PartnerStack URLs."""
from pathlib import Path
import re

# Mapping of broken links to correct PartnerStack URLs
LINK_FIXES = {
    # ClickUp fixes
    "https://partnerstack.com/go/clickup?ref=gjhblog": "https://try.web.clickup.com/f1xmsye5bi9s-ftpxvl",
    "https://try.web.clickup.com/tqnlgz13ew71": "https://try.web.clickup.com/f1xmsye5bi9s-ftpxvl",  # Old working link

    # Gusto fixes
    "https://partnerstack.com/go/gusto?ref=gjhblog": "https://get.gusto.com/703bagjmmd7u",

    # folk fixes
    "https://partnerstack.com/go/part_XW1ekbNBeTuMFu?ref=gjh-consulting": "https://try.folk.app/2adrxyae7k0c",

    # Aura fixes
    "https://partnerstack.com/go/part_3gUdr7cpniflg8?ref=gjh-consulting": "https://try.goaura.com/45egbdjtq5mn",
}

def fix_links_in_file(file_path: Path) -> tuple[int, list[str]]:
    """Fix affiliate links in a single blog post.

    Returns: (number of fixes, list of changes made)
    """
    content = file_path.read_text()
    original_content = content
    fixes_made = 0
    changes = []

    for old_link, new_link in LINK_FIXES.items():
        if old_link in content:
            content = content.replace(old_link, new_link)
            fixes_made += content.count(new_link) - original_content.count(new_link)
            changes.append(f"  {old_link}\n    → {new_link}")

    if content != original_content:
        file_path.write_text(content)

    return fixes_made, changes

def main():
    """Fix all affiliate links in blog posts."""
    posts_dir = Path("frontend/posts")
    total_files_fixed = 0
    total_links_fixed = 0

    print("="*80)
    print("FIXING AFFILIATE LINKS IN BLOG POSTS")
    print("="*80)

    for post_file in sorted(posts_dir.glob("*.md")):
        fixes_made, changes = fix_links_in_file(post_file)

        if fixes_made > 0:
            total_files_fixed += 1
            total_links_fixed += fixes_made
            print(f"\n✅ {post_file.name}")
            print(f"   Fixed {fixes_made} link(s):")
            for change in changes:
                print(change)

    print(f"\n" + "="*80)
    print(f"📊 SUMMARY:")
    print(f"   Files updated: {total_files_fixed}")
    print(f"   Total links fixed: {total_links_fixed}")
    print("="*80)

    if total_links_fixed == 0:
        print("\n⚠️  No links were fixed. All links may already be correct.")

    return total_links_fixed > 0

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
