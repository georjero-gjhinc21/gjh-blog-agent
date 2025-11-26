"""Celery tasks package."""
from .celery_app import celery_app
from .blog_tasks import (
    discover_topics_task,
    generate_blog_post_task,
    publish_scheduled_posts_task,
    update_metrics_task
)

__all__ = [
    "celery_app",
    "discover_topics_task",
    "generate_blog_post_task",
    "publish_scheduled_posts_task",
    "update_metrics_task"
]
