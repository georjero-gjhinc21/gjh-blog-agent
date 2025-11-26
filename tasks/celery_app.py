"""Celery application configuration."""
from celery import Celery
from celery.schedules import crontab
from config import settings

# Create Celery app
celery_app = Celery(
    "gjh_blog_agent",
    broker=settings.redis_url,
    backend=settings.redis_url,
    include=["tasks.blog_tasks"]
)

# Configure Celery
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes
    task_soft_time_limit=25 * 60,  # 25 minutes
)

# Schedule periodic tasks
celery_app.conf.beat_schedule = {
    # Discover new topics daily at 6 AM
    "discover-topics-daily": {
        "task": "tasks.blog_tasks.discover_topics_task",
        "schedule": crontab(hour=6, minute=0),
    },
    # Generate blog posts: Monday, Wednesday, Friday at 8 AM
    "generate-blog-monday": {
        "task": "tasks.blog_tasks.generate_blog_post_task",
        "schedule": crontab(hour=8, minute=0, day_of_week=1),  # Monday
    },
    "generate-blog-wednesday": {
        "task": "tasks.blog_tasks.generate_blog_post_task",
        "schedule": crontab(hour=8, minute=0, day_of_week=3),  # Wednesday
    },
    "generate-blog-friday": {
        "task": "tasks.blog_tasks.generate_blog_post_task",
        "schedule": crontab(hour=8, minute=0, day_of_week=5),  # Friday
    },
    # Publish scheduled posts every hour
    "publish-scheduled-posts": {
        "task": "tasks.blog_tasks.publish_scheduled_posts_task",
        "schedule": crontab(minute=0),  # Every hour
    },
    # Update metrics daily at 11 PM
    "update-metrics-daily": {
        "task": "tasks.blog_tasks.update_metrics_task",
        "schedule": crontab(hour=23, minute=0),
    },
}
