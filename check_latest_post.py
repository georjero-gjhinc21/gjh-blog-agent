#!/usr/bin/env python3
"""Check the latest post details."""
from database import get_db_session
from models.blog import BlogPost, AffiliateProduct

with get_db_session() as db:
    post = db.query(BlogPost).order_by(BlogPost.created_at.desc()).first()

    if post:
        print(f"Latest Post: {post.title}")
        print(f"  ID: {post.id}")
        print(f"  Slug: {post.slug[:80]}")
        print(f"  Word Count: {post.word_count}")
        print(f"  Status: {post.status}")
        print(f"  Keywords: {', '.join(post.seo_keywords[:5])}")
        print(f"  Affiliate Product ID: {post.affiliate_product_id}")

        if post.affiliate_product_id:
            prod = db.query(AffiliateProduct).filter_by(id=post.affiliate_product_id).first()
            if prod:
                print(f"\n  ✅ Affiliate Matched:")
                print(f"     Product: {prod.name}")
                print(f"     Category: {prod.category}")
                print(f"     Commission: {prod.commission_rate}%")
                print(f"     Link: {prod.affiliate_link}")
        else:
            print(f"\n  ⚠️  No affiliate product matched to this post")
    else:
        print("No posts found")
