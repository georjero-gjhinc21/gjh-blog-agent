"""Content Agent - Generates high-quality blog posts."""
import re
from datetime import datetime
from typing import Optional, List, Dict
from sqlalchemy.orm import Session

from models.blog import BlogPost, Topic, AffiliateProduct
from utils.ollama_client import OllamaClient
from config import settings


class ContentAgent:
    """Generates SEO-optimized blog posts with affiliate integration."""

    def __init__(self, unified_affiliate_agent=None):
        """Initialize Content Agent.

        Args:
            unified_affiliate_agent: Optional UnifiedAffiliateAgent instance for multi-network affiliate matching
        """
        self.ollama = OllamaClient()
        self.min_words = settings.min_words
        self.max_words = settings.max_words
        self.unified_affiliate = unified_affiliate_agent  # New: support for dual-network affiliates

    def generate_post(
        self,
        db: Session,
        topic: Topic,
        affiliate_product: Optional[AffiliateProduct] = None,
        use_unified_affiliates: bool = True,
        max_affiliate_matches: int = 3
    ) -> BlogPost:
        """Generate a complete blog post from a topic.

        Args:
            db: Database session
            topic: Topic to write about
            affiliate_product: Legacy single affiliate product (for backwards compatibility)
            use_unified_affiliates: Use UnifiedAffiliateAgent for multi-network matching
            max_affiliate_matches: Maximum number of affiliate programs to include
        """
        # 1. Create outline
        outline = self._create_outline(topic)

        # 2. Generate content sections
        content = self._generate_content(topic, outline, affiliate_product)

        # 3. Create SEO elements
        title = self._generate_title(topic)
        slug = self._create_slug(title)
        meta_description = self._generate_meta_description(topic, content)
        seo_keywords = self._extract_seo_keywords(topic, content)

        # 4. Add unified affiliate matches if available
        affiliate_matches = []
        if use_unified_affiliates and self.unified_affiliate:
            try:
                affiliate_matches = self.unified_affiliate.find_best_matches(
                    content=content,
                    title=title,
                    max_matches=max_affiliate_matches
                )

                if affiliate_matches:
                    # Format and append affiliate section
                    affiliate_section = self.unified_affiliate.format_affiliate_section(affiliate_matches)
                    disclosure = self.unified_affiliate.format_affiliate_disclosure()
                    content = f"{content}\n\n{affiliate_section}\n{disclosure}"
            except Exception as e:
                print(f"Warning: Unified affiliate matching failed: {e}")

        # 5. Create excerpt
        excerpt = self._create_excerpt(content)

        # 6. Calculate word count
        word_count = len(content.split())

        # 7. Create blog post
        post = BlogPost(
            title=title,
            slug=slug,
            content=content,
            excerpt=excerpt,
            word_count=word_count,
            topic_id=topic.id,
            affiliate_product_id=affiliate_product.id if affiliate_product else None,
            seo_keywords=seo_keywords,
            meta_description=meta_description,
            status="draft",
            created_at=datetime.utcnow()
        )

        db.add(post)
        db.commit()
        db.refresh(post)

        # Store affiliate match metadata for tracking (stored in post metadata field if available)
        if affiliate_matches:
            post.metadata = {
                "affiliate_matches": [
                    {
                        "name": m["name"],
                        "network": m.get("network"),
                        "score": m.get("match_score", 0)
                    }
                    for m in affiliate_matches
                ]
            }
            db.commit()

        return post

    def _create_outline(self, topic: Topic) -> str:
        """Create a blog post outline."""
        system = """You are an expert blog content strategist specializing in government contracting and technology.
Create detailed, engaging blog post outlines."""

        prompt = f"""Create a detailed outline for a blog post about:

Title: {topic.title}
Description: {topic.description}

The outline should:
- Have 5-7 main sections
- Include an introduction and conclusion
- Focus on practical, actionable information
- Be relevant to government contractors and federal agencies

Return the outline with section headings only, one per line, prefixed with ##."""

        return self.ollama.generate(prompt, system, temperature=0.7)

    def _generate_content(
        self,
        topic: Topic,
        outline: str,
        affiliate_product: Optional[AffiliateProduct]
    ) -> str:
        """Generate the full blog post content."""
        sections = [line.strip() for line in outline.split("\n") if line.strip().startswith("##")]

        content_parts = []

        # Introduction
        intro = self._generate_introduction(topic)
        content_parts.append(intro)

        # Main sections
        for section in sections:
            if "introduction" in section.lower() or "conclusion" in section.lower():
                continue  # Skip, we handle these separately

            section_content = self._generate_section(topic, section)
            content_parts.append(f"\n{section}\n\n{section_content}")

        # Add affiliate product mention if available
        if affiliate_product:
            affiliate_mention = self._generate_affiliate_section(affiliate_product, topic)
            content_parts.append(f"\n{affiliate_mention}")

        # Conclusion
        conclusion = self._generate_conclusion(topic)
        content_parts.append(f"\n## Conclusion\n\n{conclusion}")

        return "\n".join(content_parts)

    def _generate_introduction(self, topic: Topic) -> str:
        """Generate engaging introduction."""
        system = """You are an expert writer for government contracting blogs.
Write engaging, informative introductions that hook readers."""

        prompt = f"""Write a compelling introduction (150-200 words) for this blog post:

Title: {topic.title}
Description: {topic.description}

The introduction should:
- Hook the reader immediately
- Establish relevance to government contractors
- Preview the value they'll get from reading
- Be professional but conversational"""

        return self.ollama.generate(prompt, system, temperature=0.7)

    def _generate_section(self, topic: Topic, section_heading: str) -> str:
        """Generate content for a section."""
        system = """You are an expert government contracting consultant and technical writer.
Write informative, actionable content that provides real value."""

        prompt = f"""Write detailed content (200-300 words) for this section:

Blog Topic: {topic.title}
Section: {section_heading}

Requirements:
- Provide specific, actionable information
- Include examples where relevant
- Use professional but accessible language
- Focus on practical value for government contractors
- Do NOT include the section heading in your response"""

        return self.ollama.generate(prompt, system, temperature=0.7)

    def _generate_affiliate_section(self, product: AffiliateProduct, topic: Topic) -> str:
        """Generate natural affiliate product mention."""
        system = """You are a skilled content marketer who integrates product recommendations naturally.
Create helpful, non-salesy product mentions that add value."""

        prompt = f"""Write a natural product recommendation (100-150 words) that fits this blog post:

Blog Topic: {topic.title}
Product: {product.name}
Description: {product.description}

Requirements:
- Focus on how the product solves problems discussed in the article
- Be helpful, not salesy
- Include a natural call-to-action
- Use markdown link format: [product name]({product.affiliate_link})"""

        return self.ollama.generate(prompt, system, temperature=0.7)

    def _generate_conclusion(self, topic: Topic) -> str:
        """Generate conclusion."""
        system = """You are an expert blog writer. Create conclusions that reinforce key points and inspire action."""

        prompt = f"""Write a strong conclusion (100-150 words) for this blog post:

Topic: {topic.title}
Description: {topic.description}

The conclusion should:
- Summarize key takeaways
- Reinforce the value provided
- End with a call-to-action or thought-provoking question"""

        return self.ollama.generate(prompt, system, temperature=0.7)

    def _generate_title(self, topic: Topic) -> str:
        """Generate SEO-optimized title."""
        system = """You are an SEO expert. Create compelling, click-worthy titles that rank well."""

        prompt = f"""Create an SEO-optimized blog post title based on:

Original: {topic.title}
Description: {topic.description}

Requirements:
- 50-60 characters
- Include primary keyword
- Be compelling and clickable
- Professional tone

Return ONLY the title, nothing else."""

        title = self.ollama.generate(prompt, system, temperature=0.7)
        return title.strip().strip('"').strip("'")[:100]

    def _create_slug(self, title: str) -> str:
        """Create URL slug from title."""
        slug = title.lower()
        slug = re.sub(r'[^a-z0-9\s-]', '', slug)
        slug = re.sub(r'\s+', '-', slug)
        slug = slug.strip('-')
        return slug[:100]

    def _generate_meta_description(self, topic: Topic, content: str) -> str:
        """Generate meta description."""
        system = """You are an SEO expert. Create compelling meta descriptions that drive clicks."""

        prompt = f"""Create a meta description (150-160 characters) for:

Title: {topic.title}
Content preview: {content[:500]}

Requirements:
- 150-160 characters
- Include primary keyword
- Be compelling
- Accurate to content

Return ONLY the meta description."""

        meta = self.ollama.generate(prompt, system, temperature=0.5)
        return meta.strip()[:300]

    def _extract_seo_keywords(self, topic: Topic, content: str) -> list:
        """Extract SEO keywords."""
        # Combine topic keywords with extracted content keywords
        keywords = list(topic.keywords or [])

        # Extract from content
        content_keywords = self.ollama.extract_keywords(content[:1000], max_keywords=5)
        keywords.extend(content_keywords)

        # Deduplicate
        return list(set(keywords))[:15]

    def _create_excerpt(self, content: str) -> str:
        """Create post excerpt from content."""
        # Take first paragraph
        paragraphs = content.split("\n\n")
        for para in paragraphs:
            if len(para) > 100 and not para.startswith("#"):
                excerpt = para[:250]
                # Cut at last complete sentence
                last_period = excerpt.rfind(".")
                if last_period > 0:
                    excerpt = excerpt[:last_period + 1]
                return excerpt

        return content[:250] + "..."
