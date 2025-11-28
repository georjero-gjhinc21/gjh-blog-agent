#!/usr/bin/env python3
"""Test product matching with real data."""
from database import get_db_session
from agents.affiliate_agent import AffiliateAgent
from models.blog import Topic, AffiliateProduct

# Test topics
test_topics = [
    {
        "title": "Top Project Management Tools for Government Contractors",
        "description": "Compare the best project management software for federal contractors",
        "keywords": ["project management", "software", "tools", "collaboration"]
    },
    {
        "title": "Cybersecurity Compliance for Federal Contractors",
        "description": "Essential cybersecurity tools and practices for CMMC compliance",
        "keywords": ["cybersecurity", "compliance", "security", "CMMC", "NIST"]
    },
    {
        "title": "HR and Payroll Solutions for Small Businesses",
        "description": "Streamline HR operations with modern payroll software",
        "keywords": ["hr", "payroll", "human resources", "small business"]
    },
    {
        "title": "AI-Powered Sales and Marketing Automation",
        "description": "Boost your sales with AI-driven marketing tools",
        "keywords": ["ai", "sales", "marketing", "automation", "crm"]
    }
]

agent = AffiliateAgent()

with get_db_session() as db:
    print("Testing Product Matching\n" + "="*60)

    for topic_data in test_topics:
        # Create temporary topic
        topic = Topic(
            title=topic_data["title"],
            description=topic_data["description"],
            keywords=topic_data["keywords"],
            trend_score=0.8,
            used=False
        )

        print(f"\nTopic: {topic.title}")
        print(f"Keywords: {', '.join(topic.keywords)}")

        # Find matching product
        product = agent.match_product_to_topic(db, topic)

        if product:
            print(f"✓ Matched Product: {product.name}")
            print(f"  Category: {product.category}")
            print(f"  Commission: {product.commission_rate}%")
            print(f"  Link: {product.affiliate_link[:60]}...")
        else:
            print("✗ No matching product found")

    print(f"\n" + "="*60)
    print("\nAffiliate Products Summary:")
    products = db.query(AffiliateProduct).filter_by(active=True).all()
    print(f"Total active products: {len(products)}")

    # Group by category
    categories = {}
    for p in products:
        cat = p.category
        categories[cat] = categories.get(cat, 0) + 1

    print("\nProducts by category:")
    for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"  {cat}: {count}")
