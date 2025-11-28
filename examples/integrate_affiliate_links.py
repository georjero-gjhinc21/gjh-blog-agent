#!/usr/bin/env python3
"""
Example: Integrate Unified Affiliate System with Blog Generation

This script demonstrates how to add affiliate links to your blog posts
using the dual-network affiliate system (PartnerStack + Impact.com).
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.unified_affiliate_agent import UnifiedAffiliateAgent


# ===== EXAMPLE 1: Add Affiliate Links to Existing Content =====

def add_affiliate_links_to_post(title: str, content: str) -> str:
    """Add intelligent affiliate links to a blog post.

    Args:
        title: Blog post title
        content: Blog post content (markdown)

    Returns:
        Enhanced content with affiliate section
    """
    # Initialize agent
    agent = UnifiedAffiliateAgent()

    # Find best matching programs (across both networks)
    matches = agent.find_best_matches(
        content=content,
        title=title,
        max_matches=3,  # Add 3 affiliate links
        min_score=0.15  # Minimum relevance score
    )

    if not matches:
        print("No relevant affiliate programs found")
        return content

    # Format affiliate section
    affiliate_section = agent.format_affiliate_section(
        matches,
        section_title="Recommended Tools & Services"
    )

    # Add disclosure
    disclosure = agent.format_affiliate_disclosure()

    # Combine everything
    enhanced_content = f"{content}\n\n{affiliate_section}\n{disclosure}"

    return enhanced_content


# ===== EXAMPLE 2: Generate Post with Specific Product =====

def create_post_for_product(product_name: str, topic: str) -> dict:
    """Create a blog post featuring a specific affiliate product.

    Args:
        product_name: Name of the product to feature
        topic: Blog post topic/angle

    Returns:
        Dict with post content and affiliate link
    """
    agent = UnifiedAffiliateAgent()
    agent.sync_all_programs()

    # Get the specific product
    product = agent.get_program_by_name(product_name)

    if not product:
        print(f"Product '{product_name}' not found")
        return None

    # Generate affiliate link
    link = agent.generate_link(
        program_name=product['name'],
        sub_id=topic.lower().replace(' ', '-')
    )

    return {
        'product': product,
        'link': link,
        'network': product.get('network'),
        'commission': product.get('commission_rate', 0)
    }


# ===== EXAMPLE 3: Integration with Batch Post Generation =====

def enhance_batch_posts(posts: list) -> list:
    """Add affiliate links to a batch of blog posts.

    Args:
        posts: List of post dicts with 'title' and 'content'

    Returns:
        Enhanced posts with affiliate links
    """
    agent = UnifiedAffiliateAgent()
    agent.sync_all_programs()

    enhanced_posts = []

    for post in posts:
        # Find matches
        matches = agent.find_best_matches(
            content=post.get('content', ''),
            title=post.get('title', ''),
            max_matches=3
        )

        # Add affiliate section
        if matches:
            affiliate_section = agent.format_affiliate_section(matches)
            disclosure = agent.format_affiliate_disclosure()

            post['content'] = f"{post['content']}\n\n{affiliate_section}\n{disclosure}"
            post['affiliate_programs'] = [
                {
                    'name': m['name'],
                    'network': m.get('network'),
                    'score': m.get('match_score', 0)
                }
                for m in matches
            ]

        enhanced_posts.append(post)

    return enhanced_posts


# ===== EXAMPLE 4: Smart Product Recommendation =====

def get_product_recommendations(
    category: str = None,
    keyword: str = None,
    min_commission: float = 0
) -> list:
    """Get affiliate product recommendations based on criteria.

    Args:
        category: Filter by category (e.g., "Cybersecurity")
        keyword: Search keyword
        min_commission: Minimum commission rate

    Returns:
        List of recommended products
    """
    agent = UnifiedAffiliateAgent()
    agent.sync_all_programs()

    # Search or get all
    if keyword:
        products = agent.search_programs(keyword, limit=20)
    else:
        products = agent.list_all_programs()

    # Filter by criteria
    filtered = []
    for prod in products:
        # Category filter
        if category and category.lower() not in prod.get('category', '').lower():
            continue

        # Commission filter
        if prod.get('commission_rate', 0) < min_commission:
            continue

        filtered.append(prod)

    return filtered


# ===== EXAMPLE 5: Integration with Your generate_batch_posts.py =====

def integrate_with_batch_generation():
    """
    Example of how to modify your existing generate_batch_posts.py
    to automatically include affiliate links.
    """

    # In your generate_batch_posts.py, after generating content:

    agent = UnifiedAffiliateAgent()

    # For each post in your BATCH_POSTS
    for post_config in BATCH_POSTS:  # Your existing BATCH_POSTS list
        # Generate the blog content (your existing logic)
        # content = generate_content(post_config)

        # Add this NEW code to include affiliate links:
        product_name = post_config.get('product_name')

        # Option A: Feature the specific product
        if product_name:
            product = agent.get_program_by_name(product_name)
            if product:
                link = agent.generate_link(
                    product_name=product['name'],
                    sub_id=post_config.get('slug')
                )
                # Insert link into content at appropriate places
                # content = content.replace(product_name, f"[{product_name}]({link})")

        # Option B: Add related products section
        # matches = agent.find_best_matches(
        #     content=content,
        #     title=post_config['title'],
        #     max_matches=3
        # )
        # affiliate_section = agent.format_affiliate_section(matches)
        # content += f"\n\n{affiliate_section}"

    print("Affiliate links integrated!")


# ===== USAGE EXAMPLES =====

if __name__ == "__main__":
    print("🔗 Affiliate Integration Examples\n" + "="*50)

    # Example 1: Enhance existing content
    print("\n1. Adding affiliate links to content...")
    sample_content = """
    Government contractors need robust cybersecurity solutions
    to meet CMMC compliance requirements. This includes endpoint
    protection, threat intelligence, and security monitoring.
    """
    enhanced = add_affiliate_links_to_post(
        title="Cybersecurity for Federal Contractors",
        content=sample_content
    )
    print(f"   ✓ Added {enhanced.count('](http') - sample_content.count('](http')} affiliate links")

    # Example 2: Get product info
    print("\n2. Getting product information...")
    product_info = create_post_for_product(
        product_name="ClickUp",
        topic="project-management-tools"
    )
    if product_info:
        print(f"   ✓ {product_info['product']['name']} ({product_info['network']})")
        print(f"   ✓ Commission: {product_info['commission']}%")

    # Example 3: Get recommendations
    print("\n3. Getting product recommendations...")
    recommendations = get_product_recommendations(
        keyword="project",
        min_commission=20
    )
    print(f"   ✓ Found {len(recommendations)} products with 20%+ commission")

    print("\n" + "="*50)
    print("✅ Integration examples completed!")
    print("\nTo integrate with your blog generation:")
    print("1. Import: from agents.unified_affiliate_agent import UnifiedAffiliateAgent")
    print("2. Initialize: agent = UnifiedAffiliateAgent()")
    print("3. Find matches: matches = agent.find_best_matches(content, title)")
    print("4. Add section: content += agent.format_affiliate_section(matches)")


# Global reference for the example
BATCH_POSTS = []  # Placeholder for example
