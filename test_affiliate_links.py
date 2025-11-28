#!/usr/bin/env python3
"""Test affiliate link generation."""
from utils.partnerstack_client import PartnerStackClient
from database import get_db_session
from models.blog import AffiliateProduct

client = PartnerStackClient()

print("Testing Affiliate Link Generation\n" + "="*60)

# Test with sample program keys
test_keys = ["clickup", "mongodb", "deel", "freshdesk"]

print("\n1. Testing generate_affiliate_link() method:")
for key in test_keys:
    link = client.generate_affiliate_link(key, path=f"blog-{key}")
    print(f"\n  {key}:")
    print(f"    {link}")

# Test with real database products
print("\n\n2. Testing with real synced products:")
with get_db_session() as db:
    products = db.query(AffiliateProduct).filter_by(active=True).limit(5).all()

    for product in products:
        print(f"\n  {product.name}:")
        print(f"    Database link: {product.affiliate_link}")
        if product.external_id:
            generated = client.generate_affiliate_link(product.external_id or product.name.lower().replace(" ", "-"))
            print(f"    Generated: {generated}")

print("\n" + "="*60)
