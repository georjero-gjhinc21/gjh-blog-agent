#!/usr/bin/env python3
"""Quick script to seed a test topic."""
from database import get_db_session
from models.blog import Topic
from datetime import datetime

with get_db_session() as db:
    # Create a government contracting topic
    topic = Topic(
        title="Best Project Management Tools for Federal Contractors in 2025",
        description="Federal contractors need robust project management solutions to handle complex government contracts. This guide explores the top project management platforms that offer compliance features, security, and collaboration tools essential for government work.",
        source_url="",
        trend_score=0.85,
        keywords=["project management", "federal contractors", "government contracts", "compliance", "collaboration", "GSA schedule"],
        created_at=datetime.utcnow(),
        used=False
    )

    db.add(topic)
    db.commit()
    db.refresh(topic)

    print(f"✓ Created topic: {topic.title}")
    print(f"  ID: {topic.id}")
    print(f"  Score: {topic.trend_score}")
    print(f"  Keywords: {', '.join(topic.keywords)}")
