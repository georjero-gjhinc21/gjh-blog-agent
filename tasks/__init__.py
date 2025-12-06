"""Celery tasks package."""
from .celery_app import celery_app
from .blog_tasks import (
    discover_topics_task,
    generate_blog_post_task,
    publish_scheduled_posts_task,
    update_metrics_task
)
# Ensure integrator task is imported for Celery auto-discovery
from .integrate_affiliates import integrate_affiliates_task

__all__ = [
    "celery_app",
    "discover_topics_task",
    "generate_blog_post_task",
    "publish_scheduled_posts_task",
    "update_metrics_task",
    "integrate_affiliates_task"
]
