#!/usr/bin/env python3
"""Check the generated post details."""
from database import get_db_session
from models.blog import BlogPost, AffiliateProduct

with get_db_session() as db:
    post = db.query(BlogPost).filter_by(
        slug='master-federal-contracts-with-top-rated-project-management-tools-in-2025'
    ).first()

    if post:
        print(f"Post: {post.title}")
        print(f"  Word Count: {post.word_count}")
        print(f"  Status: {post.status}")
        print(f"  Affiliate Product ID: {post.affiliate_product_id}")

        if post.affiliate_product_id:
            prod = db.query(AffiliateProduct).filter_by(id=post.affiliate_product_id).first()
            if prod:
                print(f"  Affiliate: {prod.name}")
                print(f"  Category: {prod.category}")
                print(f"  Commission: {prod.commission_rate}%")
                print(f"  Link: {prod.affiliate_link}")
        else:
            print("  No affiliate product matched")
    else:
        print("Post not found")
