#!/usr/bin/env python3
"""Check ClickUp product details."""
from database import get_db_session
from models.blog import AffiliateProduct

with get_db_session() as db:
    clickup = db.query(AffiliateProduct).filter_by(name="ClickUp").first()

    if clickup:
        print(f"Product: {clickup.name}")
        print(f"  ID: {clickup.id}")
        print(f"  Category: {clickup.category}")
        print(f"  Description: {clickup.description}")
        print(f"  Keywords: {clickup.relevance_keywords}")
        print(f"  Commission: {clickup.commission_rate}%")
        print(f"  Active: {clickup.active}")
    else:
        print("ClickUp not found")
