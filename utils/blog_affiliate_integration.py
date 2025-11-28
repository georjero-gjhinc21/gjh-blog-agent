#!/usr/bin/env python3
"""
Blog-Affiliate Integration Module

Drop-in module to automatically add affiliate links to blog posts.
Works with existing blog generation workflow.
"""

from agents.unified_affiliate_agent import UnifiedAffiliateAgent
from typing import Optional, Dict, List


class BlogAffiliateIntegration:
    """Integrates affiliate matching into blog generation workflow."""

    def __init__(self):
        """Initialize with unified affiliate agent."""
        self.agent = UnifiedAffiliateAgent()
        self.agent.sync_all_programs()  # Load all programs once

    def enhance_post(
        self,
        title: str,
        content: str,
        slug: str = "",
        max_matches: int = 3,
        min_score: float = 0.20
    ) -> Dict[str, str]:
        """
        Enhance a blog post with affiliate links.

        Args:
            title: Blog post title
            content: Blog post content (markdown)
            slug: Post slug for tracking (optional)
            max_matches: Maximum number of affiliate matches
            min_score: Minimum match score (0.0-1.0)

        Returns:
            Dict with enhanced content and metadata
        """
        # Find best matches
        matches = self.agent.find_best_matches(
            content=content,
            title=title,
            max_matches=max_matches,
            min_score=min_score
        )

        if not matches:
            # No matches found - return original content
            return {
                "content": content,
                "has_affiliates": False,
                "affiliate_count": 0,
                "matches": []
            }

        # Generate affiliate section
        affiliate_section = self._format_section(matches, slug)

        # Add disclosure
        disclosure = self.agent.format_affiliate_disclosure()

        # Combine
        enhanced_content = f"{content}\n\n{affiliate_section}\n{disclosure}"

        return {
            "content": enhanced_content,
            "has_affiliates": True,
            "affiliate_count": len(matches),
            "matches": [
                {
                    "name": m["name"],
                    "network": m.get("network"),
                    "score": m.get("match_score", 0),
                    "commission": m.get("commission_rate", 0)
                }
                for m in matches
            ]
        }

    def _format_section(self, matches: List[Dict], slug: str = "") -> str:
        """Format affiliate matches as a blog section."""
        section = "\n## Recommended Tools & Resources\n\n"
        section += "Based on this content, here are some tools that might help:\n\n"

        for i, match in enumerate(matches, 1):
            # Generate tracking link
            link = self.agent.generate_link(
                program_name=match["name"],
                sub_id=slug or "blog"
            )

            section += f"### {i}. {match['name']}\n\n"
            section += f"{match.get('description', 'Industry-leading solution.')}\n\n"

            if link:
                section += f"**[Learn more about {match['name']} →]({link})**\n\n"

        return section

    def add_inline_links(
        self,
        content: str,
        title: str,
        max_inline: int = 3
    ) -> str:
        """
        Add inline affiliate links within content (more subtle).

        Args:
            content: Blog post content
            title: Blog post title
            max_inline: Maximum inline links to add

        Returns:
            Content with inline affiliate links added
        """
        # Find matches
        matches = self.agent.find_best_matches(
            content=content,
            title=title,
            max_matches=max_inline,
            min_score=0.25  # Higher threshold for inline
        )

        if not matches:
            return content

        modified_content = content

        # Add inline links where product names appear
        for match in matches:
            product_name = match["name"]
            link = self.agent.generate_link(product_name)

            if link:
                # Replace first occurrence of product name with linked version
                # Only if it's not already a link
                if product_name in modified_content and f"]({link})" not in modified_content:
                    modified_content = modified_content.replace(
                        product_name,
                        f"[{product_name}]({link})",
                        1  # Only first occurrence
                    )

        return modified_content

    def get_pre_approved_links(self, category: str, count: int = 5) -> List[Dict]:
        """
        Get pre-approved affiliate links for a category.

        Useful for creating resource pages or category-specific recommendations.

        Args:
            category: Category to filter by
            count: Number of programs to return

        Returns:
            List of program dicts with links
        """
        all_programs = self.agent.list_all_programs()

        # Filter by category
        filtered = [
            p for p in all_programs
            if category.lower() in p.get("category", "").lower()
        ]

        # Sort by commission rate
        filtered.sort(key=lambda x: x.get("commission_rate", 0), reverse=True)

        # Take top N
        top_programs = filtered[:count]

        # Generate links
        results = []
        for prog in top_programs:
            link = self.agent.generate_link(prog["name"])
            results.append({
                "name": prog["name"],
                "description": prog.get("description", ""),
                "category": prog.get("category", ""),
                "commission": prog.get("commission_rate", 0),
                "network": prog.get("network", ""),
                "link": link
            })

        return results


# ===== Usage Examples =====

def example_basic_enhancement():
    """Example: Basic post enhancement."""
    integrator = BlogAffiliateIntegration()

    title = "Best Project Management Tools for Government Contractors"
    content = """
    Government contractors need robust project management solutions
    to track tasks, collaborate with teams, and meet strict deadlines...
    """

    result = integrator.enhance_post(title, content, slug="pm-tools-govcon")

    print(f"Enhanced: {result['has_affiliates']}")
    print(f"Added {result['affiliate_count']} affiliate recommendations")
    print(result['content'])


def example_inline_links():
    """Example: Add subtle inline links."""
    integrator = BlogAffiliateIntegration()

    content = """
    Many contractors use ClickUp for project management because it
    offers great collaboration features...
    """

    enhanced = integrator.add_inline_links(content, "PM Tools")
    print(enhanced)


def example_category_page():
    """Example: Create a category resource page."""
    integrator = BlogAffiliateIntegration()

    cybersecurity_tools = integrator.get_pre_approved_links("cybersecurity", count=10)

    for tool in cybersecurity_tools:
        print(f"{tool['name']}: {tool['link']}")


if __name__ == "__main__":
    # Run examples
    print("Running integration examples...\n")
    example_basic_enhancement()
