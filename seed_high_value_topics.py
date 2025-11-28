#!/usr/bin/env python3
"""Seed topics tailored to high-value affiliate products."""
from database import get_db_session
from models.blog import Topic
from datetime import datetime

# Topics tailored to high-value products
HIGH_VALUE_TOPICS = [
    # CrowdStrike (35% - Cybersecurity)
    {
        "title": "Best Cybersecurity Solutions for Federal Contractors in 2025",
        "description": "Comprehensive guide to enterprise cybersecurity platforms for government contractors",
        "keywords": ["cybersecurity", "endpoint protection", "threat detection", "compliance", "federal contractors"],
        "category": "Cybersecurity",
        "target_product": "CrowdStrike"
    },
    {
        "title": "CMMC 2.0 Compliance: Essential Cybersecurity Tools for Defense Contractors",
        "description": "Navigate CMMC requirements with enterprise-grade cybersecurity solutions",
        "keywords": ["CMMC", "cybersecurity", "defense contractors", "compliance", "endpoint security"],
        "category": "Cybersecurity",
        "target_product": "CrowdStrike"
    },

    # GetResponse (33% - Marketing)
    {
        "title": "Email Marketing Strategies for Government Contractors",
        "description": "Build effective email campaigns to win more federal contracts",
        "keywords": ["email marketing", "government contractors", "lead generation", "marketing automation"],
        "category": "Marketing",
        "target_product": "GetResponse"
    },
    {
        "title": "Marketing Automation for Small Government Contracting Firms",
        "description": "Streamline your marketing with automation tools",
        "keywords": ["marketing automation", "small business", "government contracting", "email campaigns"],
        "category": "Marketing",
        "target_product": "GetResponse"
    },

    # Cybersecurity Compliance Kit (30%)
    {
        "title": "NIST 800-171 Compliance Toolkit for Federal Contractors",
        "description": "Complete compliance framework and tools for NIST requirements",
        "keywords": ["NIST 800-171", "compliance", "cybersecurity", "federal contractors", "framework"],
        "category": "Cybersecurity",
        "target_product": "Cybersecurity Compliance Kit"
    },

    # FedBiz Pro Software (25%)
    {
        "title": "Best Contract Management Software for Federal Contractors",
        "description": "Streamline federal contract management with specialized software",
        "keywords": ["contract management", "federal contractors", "software", "compliance", "automation"],
        "category": "Software",
        "target_product": "FedBiz Pro Software"
    },

    # Gusto (25% - HR & Payroll)
    {
        "title": "HR and Payroll Solutions for Small Government Contractors",
        "description": "Simplify HR management and payroll for your contracting business",
        "keywords": ["HR", "payroll", "small business", "government contractors", "compliance"],
        "category": "HR",
        "target_product": "Gusto"
    },
    {
        "title": "Managing Remote Teams in Government Contracting",
        "description": "HR tools and best practices for distributed contractor teams",
        "keywords": ["remote work", "HR management", "team management", "government contractors"],
        "category": "HR",
        "target_product": "Gusto"
    },

    # Federal Data Analytics Platform (22%)
    {
        "title": "Federal Contracting Data Analytics: Win More Contracts with Data",
        "description": "Leverage data analytics to identify and win federal opportunities",
        "keywords": ["data analytics", "federal contracting", "market intelligence", "contract opportunities"],
        "category": "Analytics",
        "target_product": "Federal Data Analytics Platform"
    },

    # GovCon Academy Training (20%)
    {
        "title": "Essential Training for New Government Contractors",
        "description": "Master the fundamentals of federal contracting",
        "keywords": ["training", "government contracting", "certification", "education", "contractors"],
        "category": "Training",
        "target_product": "GovCon Academy Training"
    },
    {
        "title": "Advanced Government Contracting Certification Programs",
        "description": "Professional development for experienced contractors",
        "keywords": ["certification", "training", "professional development", "government contracting"],
        "category": "Training",
        "target_product": "GovCon Academy Training"
    },

    # Navan (20% - Travel & Expense)
    {
        "title": "Travel Management Solutions for Federal Contractors",
        "description": "Streamline business travel and expense reporting",
        "keywords": ["travel management", "expense reporting", "government contractors", "compliance"],
        "category": "Travel",
        "target_product": "Navan"
    },

    # SBIR/STTR Grant Writing Service (18%)
    {
        "title": "SBIR and STTR Grant Writing Guide for Small Businesses",
        "description": "Win federal research grants with expert grant writing",
        "keywords": ["SBIR", "STTR", "grant writing", "small business", "federal grants"],
        "category": "Grants",
        "target_product": "SBIR/STTR Grant Writing Service"
    },
    {
        "title": "Federal Research Funding Opportunities for Tech Startups",
        "description": "Navigate SBIR/STTR programs and secure R&D funding",
        "keywords": ["federal funding", "SBIR", "STTR", "tech startups", "research grants"],
        "category": "Grants",
        "target_product": "SBIR/STTR Grant Writing Service"
    },

    # SAM.gov Registration Service (15%)
    {
        "title": "SAM.gov Registration: Complete Guide for Federal Contractors",
        "description": "Step-by-step guide to SAM registration and maintenance",
        "keywords": ["SAM.gov", "registration", "federal contractors", "compliance", "government contracting"],
        "category": "Compliance",
        "target_product": "SAM.gov Registration Service"
    },
]

def seed_high_value_topics():
    """Seed database with topics tailored to high-value products."""
    with get_db_session() as db:
        added = 0

        for topic_data in HIGH_VALUE_TOPICS:
            # Check if topic already exists
            existing = db.query(Topic).filter_by(title=topic_data["title"]).first()
            if existing:
                continue

            # Create topic
            topic = Topic(
                title=topic_data["title"],
                description=topic_data["description"],
                keywords=topic_data["keywords"],
                trend_score=0.95,  # High score for high-value products
                source_url=f"internal://high_value/{topic_data['target_product'].lower().replace(' ', '-')}",
                used=False
            )

            db.add(topic)
            added += 1
            print(f"✓ Added: {topic.title} (for {topic_data['target_product']})")

        db.commit()
        print(f"\n✓ Seeded {added} high-value topics")

if __name__ == "__main__":
    seed_high_value_topics()
