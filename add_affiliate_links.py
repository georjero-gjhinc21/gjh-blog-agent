#!/usr/bin/env python3
"""Add affiliate links to posts that don't have them."""
from pathlib import Path
import re

# Available affiliate products with their URLs and descriptions
AFFILIATE_PRODUCTS = {
    "clickup": {
        "name": "ClickUp",
        "url": "https://try.web.clickup.com/f1xmsye5bi9s-ftpxvl",
        "description": "All-in-one project management and productivity platform for teams. Features include task management, time tracking, goals, docs, and collaboration tools perfect for government contractors.",
        "category": "Project Management",
        "keywords": ["project management", "task management", "collaboration", "productivity", "team", "deadline", "workflow", "tracking"]
    },
    "folk": {
        "name": "folk",
        "url": "https://try.folk.app/2adrxyae7k0c",
        "description": "Simple, powerful CRM for managing relationships, tracking opportunities, and staying organized with government contracts and client communications.",
        "category": "CRM & Contact Management",
        "keywords": ["crm", "contact", "relationship", "pipeline", "client", "opportunity", "communication", "organization"]
    },
    "gusto": {
        "name": "Gusto",
        "url": "https://get.gusto.com/703bagjmmd7u",
        "description": "Modern payroll, benefits, and HR platform for small businesses. Automate payroll, manage compliance, and take care of your team.",
        "category": "HR & Payroll",
        "keywords": ["hr", "payroll", "benefits", "compliance", "employee", "hiring", "onboarding", "team management"]
    },
    "drip": {
        "name": "Drip",
        "url": "https://try.drip.com/4li1ih52geep",
        "description": "Marketing automation platform designed for ecommerce and B2B businesses. Build personalized email campaigns, automate workflows, and grow your business.",
        "category": "Marketing Automation",
        "keywords": ["email marketing", "marketing automation", "campaign", "email", "newsletter", "outreach", "engagement", "lead generation"]
    },
    "getresponse": {
        "name": "GetResponse",
        "url": "https://try.getresponsetoday.com/92e3zsxnzj9w-xlkg1t",
        "description": "Complete email marketing and automation platform with landing pages, webinars, and conversion funnels to help grow your government contracting business.",
        "category": "Email Marketing",
        "keywords": ["email marketing", "automation", "landing page", "webinar", "conversion", "email campaign", "newsletter", "lead nurturing"]
    },
    "mongodb": {
        "name": "MongoDB",
        "url": "https://mongodb.partnerlinks.io/fvfld1r9i7px",
        "description": "Modern database platform for building applications. Flexible document model, scalable architecture, and powerful querying for government contractors managing complex data.",
        "category": "Database & Infrastructure",
        "keywords": ["database", "data", "storage", "cloud", "infrastructure", "application", "scalability", "tech stack"]
    },
}

def get_post_content_sample(file_path: Path) -> str:
    """Get first 1000 chars of post content for analysis."""
    content = file_path.read_text()
    # Remove frontmatter
    content = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)
    return content[:1000].lower()

def select_best_product(file_path: Path) -> dict:
    """Select the most appropriate affiliate product for a post."""
    filename = file_path.name.lower()
    content_sample = get_post_content_sample(file_path)
    combined_text = filename + " " + content_sample

    # Score each product based on keyword matches
    scores = {}
    for product_id, product in AFFILIATE_PRODUCTS.items():
        score = 0
        for keyword in product["keywords"]:
            if keyword in combined_text:
                score += 1
        scores[product_id] = score

    # Get product with highest score
    if max(scores.values()) > 0:
        best_product_id = max(scores, key=scores.get)
        return AFFILIATE_PRODUCTS[best_product_id]

    # Default to ClickUp for general project/contract management
    return AFFILIATE_PRODUCTS["clickup"]

def has_affiliate_link(content: str) -> bool:
    """Check if post already has an affiliate link."""
    return "🔗 [Try" in content or "affiliate" in content.lower()

def add_affiliate_section(file_path: Path, product: dict) -> bool:
    """Add affiliate section to a blog post."""
    content = file_path.read_text()

    if has_affiliate_link(content):
        return False

    # Create affiliate section
    affiliate_section = f"""
## Recommended Tool

**{product['name']}** - {product['description']}

🔗 [Try {product['name']} Today]({product['url']})

*Category: {product['category']}*

---
"""

    # Find the best place to insert (before the last heading or at the end)
    # Look for common ending patterns
    patterns = [
        r'\n## Conclusion\n',
        r'\n## Summary\n',
        r'\n## Final Thoughts\n',
        r'\n## Wrapping Up\n',
        r'\n## Next Steps\n',
    ]

    inserted = False
    for pattern in patterns:
        if re.search(pattern, content):
            content = re.sub(pattern, f'\n{affiliate_section}\n## ', content, count=1)
            inserted = True
            break

    # If no conclusion section found, add before the last paragraph
    if not inserted:
        # Add before the last line
        lines = content.rstrip().split('\n')
        # Find last heading
        last_heading_idx = -1
        for i in range(len(lines) - 1, -1, -1):
            if lines[i].startswith('#'):
                last_heading_idx = i
                break

        if last_heading_idx > 0:
            lines.insert(last_heading_idx, affiliate_section.strip())
            content = '\n'.join(lines) + '\n'
        else:
            # Just add at the end
            content = content.rstrip() + '\n\n' + affiliate_section

    file_path.write_text(content)
    return True

def main():
    """Add affiliate links to posts without them."""
    posts_dir = Path("frontend/posts")

    print("="*80)
    print("ADDING AFFILIATE LINKS TO POSTS")
    print("="*80)

    # Get posts without affiliate links
    posts_without_links = []
    for post_file in sorted(posts_dir.glob("*.md")):
        content = post_file.read_text()
        if not has_affiliate_link(content):
            posts_without_links.append(post_file)

    print(f"\n📊 Found {len(posts_without_links)} posts without affiliate links")
    print(f"🎯 Adding relevant affiliate products to each post...\n")

    added_count = 0
    product_usage = {}

    for post_file in posts_without_links:
        product = select_best_product(post_file)

        if add_affiliate_section(post_file, product):
            added_count += 1
            product_usage[product['name']] = product_usage.get(product['name'], 0) + 1
            print(f"✅ {post_file.name}")
            print(f"   Added: {product['name']} ({product['category']})")
        else:
            print(f"⏭️  {post_file.name}")
            print(f"   Skipped: Already has affiliate link")

    print(f"\n" + "="*80)
    print(f"📊 SUMMARY:")
    print(f"   Posts updated: {added_count}")
    print(f"\n   Products used:")
    for product_name, count in sorted(product_usage.items(), key=lambda x: x[1], reverse=True):
        print(f"     {product_name}: {count} posts")
    print("="*80)

    return added_count

if __name__ == "__main__":
    count = main()
    exit(0 if count > 0 else 1)
