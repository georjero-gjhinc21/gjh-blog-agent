"""Celery tasks for blog generation workflow."""
from datetime import datetime, timedelta
from .celery_app import celery_app
from database import get_db_session
from agents import (
    ResearchAgent,
    AffiliateAgent,
    ContentAgent,
    PublishingAgent,
    MonitoringAgent
)


@celery_app.task(name="tasks.blog_tasks.discover_topics_task")
def discover_topics_task():
    """Discover new trending topics."""
    print("Starting topic discovery...")

    with get_db_session() as db:
        research_agent = ResearchAgent()
        topics = research_agent.discover_topics(db, max_topics=10)

        print(f"✓ Discovered {len(topics)} new topics")
        for topic in topics:
            print(f"  - {topic.title} (score: {topic.trend_score:.2f})")

        return {
            "topics_discovered": len(topics),
            "topics": [t.title for t in topics]
        }


@celery_app.task(name="tasks.blog_tasks.generate_blog_post_task")
def generate_blog_post_task():
    """Generate a new blog post from available topics."""
    print("Starting blog post generation...")

    with get_db_session() as db:
        # Initialize agents
        research_agent = ResearchAgent()
        affiliate_agent = AffiliateAgent()
        content_agent = ContentAgent()
        publishing_agent = PublishingAgent()

        # 1. Get unused topic
        topic = research_agent.get_unused_topic(db)
        if not topic:
            print("✗ No unused topics available")
            return {"error": "No topics available"}

        print(f"✓ Selected topic: {topic.title}")

        # 2. Match affiliate product
        affiliate_product = affiliate_agent.match_product_to_topic(db, topic)
        if affiliate_product:
            print(f"✓ Matched product: {affiliate_product.name}")
        else:
            print("  No affiliate product matched")

        # 3. Generate blog post
        print("  Generating content...")
        post = content_agent.generate_post(db, topic, affiliate_product)
        print(f"✓ Generated post: {post.title} ({post.word_count} words)")

        # 4. Mark topic as used
        research_agent.mark_topic_used(db, topic.id)

        # 5. Schedule for publication (publish immediately or schedule)
        # For automated workflow, publish immediately
        success = publishing_agent.publish_post(db, post)

        if success:
            return {
                "post_id": post.id,
                "title": post.title,
                "url": post.vercel_url,
                "word_count": post.word_count,
                "status": "published"
            }
        else:
            return {
                "post_id": post.id,
                "title": post.title,
                "status": "failed"
            }


@celery_app.task(name="tasks.blog_tasks.publish_scheduled_posts_task")
def publish_scheduled_posts_task():
    """Publish posts that are scheduled for now or earlier."""
    print("Checking for scheduled posts...")

    with get_db_session() as db:
        publishing_agent = PublishingAgent()
        publishing_agent.publish_scheduled_posts(db)

        return {"status": "complete"}


@celery_app.task(name="tasks.blog_tasks.update_metrics_task")
def update_metrics_task():
    """Update performance metrics for all posts."""
    print("Updating metrics...")

    with get_db_session() as db:
        monitoring_agent = MonitoringAgent()

        # In production, this would fetch real analytics data
        # For now, simulate traffic for testing
        monitoring_agent.simulate_traffic(db)

        # Generate report
        report = monitoring_agent.generate_report(db)
        print(report)

        return {"status": "complete"}
