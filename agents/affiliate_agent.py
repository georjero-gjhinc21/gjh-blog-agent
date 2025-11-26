"""Affiliate Agent - Matches PartnerStack products to blog topics."""
from typing import Optional, List
from sqlalchemy.orm import Session

from models.blog import AffiliateProduct, Topic
from utils.ollama_client import OllamaClient
from config import settings


class AffiliateAgent:
    """Matches affiliate products to blog topics for revenue generation."""

    def __init__(self):
        """Initialize Affiliate Agent."""
        self.ollama = OllamaClient()

    def match_product_to_topic(self, db: Session, topic: Topic) -> Optional[AffiliateProduct]:
        """Find the best matching affiliate product for a topic."""
        # Get all active products
        products = db.query(AffiliateProduct).filter_by(active=True).all()

        if not products:
            # No products in database, return None
            return None

        # Score each product
        best_product = None
        best_score = 0.0

        for product in products:
            score = self._calculate_match_score(topic, product)
            if score > best_score:
                best_score = score
                best_product = product

        # Only return if score is above threshold
        return best_product if best_score > 0.4 else None

    def _calculate_match_score(self, topic: Topic, product: AffiliateProduct) -> float:
        """Calculate how well a product matches a topic."""
        # Combine topic and product information
        topic_text = f"{topic.title}\n{topic.description}\nKeywords: {', '.join(topic.keywords or [])}"
        product_text = f"{product.name}\n{product.description}\nCategory: {product.category}\nKeywords: {', '.join(product.relevance_keywords or [])}"

        system = """You are an affiliate marketing expert specializing in matching products to content.
Analyze how well a product fits with a blog topic."""

        prompt = f"""Analyze how well this product matches the blog topic.
Return ONLY a number between 0.0 and 1.0, where:
- 0.0 = no match at all
- 0.5 = moderate match
- 1.0 = perfect match

Topic:
{topic_text}

Product:
{product_text}

Match score:"""

        try:
            response = self.ollama.generate(prompt, system, temperature=0.3)
            score = float(response.strip())
            return max(0.0, min(1.0, score))
        except:
            # Fallback: keyword overlap
            topic_keywords = set([k.lower() for k in (topic.keywords or [])])
            product_keywords = set([k.lower() for k in (product.relevance_keywords or [])])

            if not topic_keywords or not product_keywords:
                return 0.0

            overlap = len(topic_keywords & product_keywords)
            total = len(topic_keywords | product_keywords)

            return overlap / total if total > 0 else 0.0

    def add_product(
        self,
        db: Session,
        name: str,
        description: str,
        category: str,
        affiliate_link: str,
        commission_rate: float = 0.0,
        relevance_keywords: List[str] = None
    ) -> AffiliateProduct:
        """Add a new affiliate product to the database."""
        product = AffiliateProduct(
            name=name,
            description=description,
            category=category,
            affiliate_link=affiliate_link,
            commission_rate=commission_rate,
            relevance_keywords=relevance_keywords or [],
            active=True
        )

        db.add(product)
        db.commit()
        db.refresh(product)

        return product

    def seed_sample_products(self, db: Session):
        """Seed database with sample affiliate products."""
        sample_products = [
            {
                "name": "SAM.gov Registration Service",
                "description": "Professional SAM.gov registration and renewal service for government contractors. Ensures compliance and active status.",
                "category": "Government Contracting Services",
                "affiliate_link": "https://partner.link/sam-registration",
                "commission_rate": 15.0,
                "relevance_keywords": ["SAM", "government contracting", "registration", "federal", "procurement"]
            },
            {
                "name": "GovCon Academy Training",
                "description": "Comprehensive online courses for government contractors covering GSA schedules, proposal writing, and compliance.",
                "category": "Training & Education",
                "affiliate_link": "https://partner.link/govcon-academy",
                "commission_rate": 20.0,
                "relevance_keywords": ["training", "GSA", "proposals", "compliance", "education", "certification"]
            },
            {
                "name": "FedBiz Pro Software",
                "description": "All-in-one software for federal contractors: opportunity tracking, proposal management, and compliance monitoring.",
                "category": "Software & Tools",
                "affiliate_link": "https://partner.link/fedbiz-pro",
                "commission_rate": 25.0,
                "relevance_keywords": ["software", "tracking", "proposals", "compliance", "automation", "CRM"]
            },
            {
                "name": "Cybersecurity Compliance Kit",
                "description": "CMMC and NIST 800-171 compliance toolkit with templates, policies, and implementation guides.",
                "category": "Cybersecurity",
                "affiliate_link": "https://partner.link/cyber-compliance",
                "commission_rate": 30.0,
                "relevance_keywords": ["cybersecurity", "CMMC", "NIST", "compliance", "security", "defense"]
            },
            {
                "name": "SBIR/STTR Grant Writing Service",
                "description": "Professional grant writing and consulting for SBIR/STTR applications with proven success rate.",
                "category": "Grant Services",
                "affiliate_link": "https://partner.link/sbir-grants",
                "commission_rate": 18.0,
                "relevance_keywords": ["SBIR", "STTR", "grants", "R&D", "innovation", "small business"]
            },
            {
                "name": "Federal Data Analytics Platform",
                "description": "Advanced analytics platform for federal spending data, contract awards, and market intelligence.",
                "category": "Data & Analytics",
                "affiliate_link": "https://partner.link/fed-analytics",
                "commission_rate": 22.0,
                "relevance_keywords": ["analytics", "data", "intelligence", "federal", "contracts", "insights"]
            }
        ]

        for product_data in sample_products:
            # Check if already exists
            existing = db.query(AffiliateProduct).filter_by(name=product_data["name"]).first()
            if not existing:
                self.add_product(db, **product_data)

        db.commit()
