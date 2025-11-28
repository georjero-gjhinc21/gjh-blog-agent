#!/usr/bin/env python3
"""Remove empty headings from blog posts."""
from pathlib import Path
import re

def cleanup_file(file_path: Path) -> bool:
    """Remove empty headings from a file."""
    content = file_path.read_text()
    original = content

    # Remove empty headings (## followed by whitespace or newline)
    content = re.sub(r'\n## *\n', '\n', content)
    content = re.sub(r'\n### *\n', '\n', content)

    # Remove multiple consecutive newlines
    content = re.sub(r'\n{3,}', '\n\n', content)

    if content != original:
        file_path.write_text(content)
        return True
    return False

def main():
    """Clean up all blog posts."""
    posts_dir = Path("frontend/posts")
    cleaned_count = 0

    print("="*80)
    print("CLEANING UP EMPTY HEADINGS")
    print("="*80)

    for post_file in sorted(posts_dir.glob("*.md")):
        if cleanup_file(post_file):
            cleaned_count += 1
            print(f"✅ {post_file.name}")

    print(f"\n{'='*80}")
    print(f"📊 Cleaned {cleaned_count} files")
    print("="*80)

    return cleaned_count

if __name__ == "__main__":
    count = main()
    exit(0)
