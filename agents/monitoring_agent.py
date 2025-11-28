"""Monitoring Agent - Tracks blog performance and revenue."""
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from collections import defaultdict

from models.blog import BlogPost, PostMetrics, Topic, AffiliateProduct


class MonitoringAgent:
    """Monitors blog performance, traffic, and affiliate revenue."""

    def __init__(self, unified_affiliate_agent=None):
        """Initialize Monitoring Agent.

        Args:
            unified_affiliate_agent: Optional UnifiedAffiliateAgent for dual-network tracking
        """
        self.unified_affiliate = unified_affiliate_agent

    def get_performance_summary(self, db: Session, days: int = 30) -> Dict:
        """Get overall performance summary."""
        cutoff_date = datetime.utcnow() - timedelta(days=days)

        # Get posts published in period
        posts = db.query(BlogPost)\
            .filter(BlogPost.published_at >= cutoff_date)\
            .filter(BlogPost.status == "published")\
            .all()

        total_posts = len(posts)
        total_views = 0
        total_clicks = 0
        total_revenue = 0.0

        for post in posts:
            if post.metrics:
                total_views += post.metrics.page_views
                total_clicks += post.metrics.affiliate_clicks
                total_revenue += post.metrics.affiliate_revenue

        return {
            "period_days": days,
            "total_posts": total_posts,
            "total_views": total_views,
            "total_affiliate_clicks": total_clicks,
            "total_revenue": total_revenue,
            "avg_views_per_post": total_views / total_posts if total_posts > 0 else 0,
            "avg_revenue_per_post": total_revenue / total_posts if total_posts > 0 else 0,
            "click_through_rate": (total_clicks / total_views * 100) if total_views > 0 else 0
        }

    def get_top_performing_posts(self, db: Session, limit: int = 10) -> List[Dict]:
        """Get top performing posts by views."""
        posts = db.query(BlogPost)\
            .join(PostMetrics)\
            .filter(BlogPost.status == "published")\
            .order_by(PostMetrics.page_views.desc())\
            .limit(limit)\
            .all()

        return [
            {
                "id": post.id,
                "title": post.title,
                "url": post.vercel_url,
                "views": post.metrics.page_views if post.metrics else 0,
                "revenue": post.metrics.affiliate_revenue if post.metrics else 0,
                "published_at": post.published_at.isoformat() if post.published_at else None
            }
            for post in posts
        ]

    def get_top_revenue_posts(self, db: Session, limit: int = 10) -> List[Dict]:
        """Get top revenue-generating posts."""
        posts = db.query(BlogPost)\
            .join(PostMetrics)\
            .filter(BlogPost.status == "published")\
            .order_by(PostMetrics.affiliate_revenue.desc())\
            .limit(limit)\
            .all()

        return [
            {
                "id": post.id,
                "title": post.title,
                "url": post.vercel_url,
                "revenue": post.metrics.affiliate_revenue if post.metrics else 0,
                "clicks": post.metrics.affiliate_clicks if post.metrics else 0,
                "conversions": post.metrics.affiliate_conversions if post.metrics else 0,
                "published_at": post.published_at.isoformat() if post.published_at else None
            }
            for post in posts
        ]

    def update_post_metrics(
        self,
        db: Session,
        post_id: int,
        page_views: int = 0,
        unique_visitors: int = 0,
        affiliate_clicks: int = 0,
        affiliate_conversions: int = 0,
        affiliate_revenue: float = 0.0
    ):
        """Update metrics for a post."""
        post = db.query(BlogPost).filter_by(id=post_id).first()
        if not post:
            return

        # Get or create metrics
        metrics = post.metrics
        if not metrics:
            metrics = PostMetrics(post_id=post_id)
            db.add(metrics)

        # Update values (additive)
        metrics.page_views += page_views
        metrics.unique_visitors += unique_visitors
        metrics.affiliate_clicks += affiliate_clicks
        metrics.affiliate_conversions += affiliate_conversions
        metrics.affiliate_revenue += affiliate_revenue
        metrics.last_updated = datetime.utcnow()

        db.commit()

    def simulate_traffic(self, db: Session):
        """Simulate traffic and metrics for testing (mock data)."""
        import random

        published_posts = db.query(BlogPost)\
            .filter(BlogPost.status == "published")\
            .all()

        for post in published_posts:
            # Simulate some traffic
            views = random.randint(50, 500)
            clicks = int(views * random.uniform(0.02, 0.08))
            conversions = int(clicks * random.uniform(0.05, 0.15))
            revenue = conversions * random.uniform(20, 100)

            self.update_post_metrics(
                db,
                post.id,
                page_views=views,
                unique_visitors=int(views * 0.7),
                affiliate_clicks=clicks,
                affiliate_conversions=conversions,
                affiliate_revenue=revenue
            )

        print(f"✓ Simulated traffic for {len(published_posts)} posts")

    def get_topic_performance(self, db: Session) -> List[Dict]:
        """Analyze which topics perform best."""
        # Get topics with published posts
        topics = db.query(Topic)\
            .join(BlogPost)\
            .filter(BlogPost.status == "published")\
            .all()

        topic_stats = []

        for topic in topics:
            posts = [p for p in topic.blog_posts if p.status == "published"]
            if not posts:
                continue

            total_views = sum(p.metrics.page_views if p.metrics else 0 for p in posts)
            total_revenue = sum(p.metrics.affiliate_revenue if p.metrics else 0 for p in posts)

            topic_stats.append({
                "topic": topic.title,
                "posts_count": len(posts),
                "total_views": total_views,
                "total_revenue": total_revenue,
                "avg_views_per_post": total_views / len(posts),
                "avg_revenue_per_post": total_revenue / len(posts)
            })

        # Sort by revenue
        topic_stats.sort(key=lambda x: x["total_revenue"], reverse=True)

        return topic_stats

    def get_affiliate_product_performance(self, db: Session) -> List[Dict]:
        """Analyze affiliate product performance."""
        products = db.query(AffiliateProduct).all()

        product_stats = []

        for product in products:
            posts = product.blog_posts
            if not posts:
                continue

            total_clicks = sum(p.metrics.affiliate_clicks if p.metrics else 0 for p in posts)
            total_conversions = sum(p.metrics.affiliate_conversions if p.metrics else 0 for p in posts)
            total_revenue = sum(p.metrics.affiliate_revenue if p.metrics else 0 for p in posts)

            conversion_rate = (total_conversions / total_clicks * 100) if total_clicks > 0 else 0

            product_stats.append({
                "product": product.name,
                "posts_count": len(posts),
                "total_clicks": total_clicks,
                "total_conversions": total_conversions,
                "total_revenue": total_revenue,
                "conversion_rate": conversion_rate,
                "avg_revenue_per_conversion": total_revenue / total_conversions if total_conversions > 0 else 0
            })

        # Sort by revenue
        product_stats.sort(key=lambda x: x["total_revenue"], reverse=True)

        return product_stats

    def generate_report(self, db: Session) -> str:
        """Generate a comprehensive performance report."""
        summary = self.get_performance_summary(db, days=30)
        top_posts = self.get_top_performing_posts(db, limit=5)
        revenue_posts = self.get_top_revenue_posts(db, limit=5)

        report = f"""
# GJH Consulting Blog Performance Report
Generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}

## 30-Day Summary
- Total Posts Published: {summary['total_posts']}
- Total Page Views: {summary['total_views']:,}
- Total Affiliate Clicks: {summary['total_affiliate_clicks']}
- Total Revenue: ${summary['total_revenue']:.2f}
- Avg Views/Post: {summary['avg_views_per_post']:.0f}
- Avg Revenue/Post: ${summary['avg_revenue_per_post']:.2f}
- Click-Through Rate: {summary['click_through_rate']:.2f}%

## Top 5 Posts by Traffic
"""
        for i, post in enumerate(top_posts, 1):
            report += f"{i}. {post['title']} - {post['views']:,} views\n"

        report += "\n## Top 5 Posts by Revenue\n"
        for i, post in enumerate(revenue_posts, 1):
            report += f"{i}. {post['title']} - ${post['revenue']:.2f}\n"

        return report

    def get_unified_affiliate_performance(self, db: Session) -> Dict:
        """Get performance metrics for dual-network affiliate system.

        Analyzes affiliate matches stored in post metadata to track
        which networks and programs perform best.

        Returns:
            Dict with network performance, top programs, conversion rates
        """
        # Get all posts with affiliate matches
        posts = db.query(BlogPost)\
            .filter(BlogPost.status == "published")\
            .filter(BlogPost.metadata.isnot(None))\
            .all()

        # Track by network
        network_stats = defaultdict(lambda: {
            "posts": 0,
            "programs": set(),
            "total_views": 0,
            "total_clicks": 0,
            "total_revenue": 0.0
        })

        # Track by program
        program_stats = defaultdict(lambda: {
            "network": "",
            "posts": 0,
            "total_score": 0.0,
            "total_views": 0,
            "total_clicks": 0,
            "total_revenue": 0.0
        })

        for post in posts:
            if not post.metadata or "affiliate_matches" not in post.metadata:
                continue

            matches = post.metadata.get("affiliate_matches", [])
            post_views = post.metrics.page_views if post.metrics else 0
            post_clicks = post.metrics.affiliate_clicks if post.metrics else 0
            post_revenue = post.metrics.affiliate_revenue if post.metrics else 0

            for match in matches:
                network = match.get("network", "unknown")
                program_name = match.get("name", "Unknown")
                score = match.get("score", 0)

                # Update network stats
                network_stats[network]["posts"] += 1
                network_stats[network]["programs"].add(program_name)
                # Distribute metrics evenly across all affiliate matches in the post
                network_stats[network]["total_views"] += post_views / len(matches)
                network_stats[network]["total_clicks"] += post_clicks / len(matches)
                network_stats[network]["total_revenue"] += post_revenue / len(matches)

                # Update program stats
                program_stats[program_name]["network"] = network
                program_stats[program_name]["posts"] += 1
                program_stats[program_name]["total_score"] += score
                program_stats[program_name]["total_views"] += post_views / len(matches)
                program_stats[program_name]["total_clicks"] += post_clicks / len(matches)
                program_stats[program_name]["total_revenue"] += post_revenue / len(matches)

        # Convert to regular dicts and calculate rates
        network_summary = {}
        for network, stats in network_stats.items():
            network_summary[network] = {
                "posts": stats["posts"],
                "unique_programs": len(stats["programs"]),
                "total_views": int(stats["total_views"]),
                "total_clicks": int(stats["total_clicks"]),
                "total_revenue": stats["total_revenue"],
                "ctr": (stats["total_clicks"] / stats["total_views"] * 100) if stats["total_views"] > 0 else 0,
                "avg_revenue_per_post": stats["total_revenue"] / stats["posts"] if stats["posts"] > 0 else 0
            }

        # Get top programs by revenue
        top_programs = sorted(
            [
                {
                    "name": name,
                    "network": stats["network"],
                    "posts": stats["posts"],
                    "avg_score": stats["total_score"] / stats["posts"] if stats["posts"] > 0 else 0,
                    "total_revenue": stats["total_revenue"],
                    "total_clicks": int(stats["total_clicks"]),
                    "ctr": (stats["total_clicks"] / stats["total_views"] * 100) if stats["total_views"] > 0 else 0
                }
                for name, stats in program_stats.items()
            ],
            key=lambda x: x["total_revenue"],
            reverse=True
        )[:10]

        return {
            "network_summary": network_summary,
            "top_programs": top_programs,
            "total_posts_with_affiliates": len([p for p in posts if p.metadata and "affiliate_matches" in p.metadata]),
            "total_affiliate_programs_used": len(program_stats)
        }

    def get_network_comparison(self, db: Session) -> Dict:
        """Compare PartnerStack vs Impact.com performance.

        Returns:
            Dict with side-by-side comparison of both networks
        """
        unified_stats = self.get_unified_affiliate_performance(db)
        network_summary = unified_stats.get("network_summary", {})

        ps_stats = network_summary.get("partnerstack", {
            "posts": 0,
            "total_revenue": 0.0,
            "total_clicks": 0,
            "ctr": 0
        })

        impact_stats = network_summary.get("impact", {
            "posts": 0,
            "total_revenue": 0.0,
            "total_clicks": 0,
            "ctr": 0
        })

        return {
            "partnerstack": ps_stats,
            "impact": impact_stats,
            "comparison": {
                "revenue_ratio": ps_stats["total_revenue"] / impact_stats["total_revenue"] if impact_stats["total_revenue"] > 0 else float('inf'),
                "posts_ratio": ps_stats["posts"] / impact_stats["posts"] if impact_stats["posts"] > 0 else float('inf'),
                "better_ctr": "partnerstack" if ps_stats["ctr"] > impact_stats["ctr"] else "impact",
                "total_revenue": ps_stats["total_revenue"] + impact_stats["total_revenue"]
            }
        }
