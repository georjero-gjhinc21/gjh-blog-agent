"""Publishing Agent - Deploys blog posts to Vercel."""
import json
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Optional
from sqlalchemy.orm import Session

from models.blog import BlogPost
from config import settings


class PublishingAgent:
    """Manages blog post deployment to Vercel (gjhconsulting.net)."""

    def __init__(self):
        """Initialize Publishing Agent."""
        self.vercel_token = settings.vercel_token
        self.project_id = settings.vercel_project_id
        self.domain = settings.blog_domain

    def publish_post(self, db: Session, post: BlogPost) -> bool:
        """Publish a blog post to Vercel."""
        try:
            # 1. Create markdown file
            post_file = self._create_post_file(post)

            # 2. Generate Vercel deployment (mock for now)
            # In production, this would:
            # - Commit to git repo
            # - Trigger Vercel deployment via API or git push
            # - Wait for deployment confirmation

            vercel_url = f"https://{self.domain}/blog/{post.slug}"

            # 3. Update post record
            post.vercel_url = vercel_url
            post.deployed = True
            post.published_at = datetime.utcnow()
            post.status = "published"

            db.commit()

            print(f"✓ Published: {post.title}")
            print(f"  URL: {vercel_url}")

            return True

        except Exception as e:
            print(f"✗ Publishing failed: {e}")
            return False

    def _create_post_file(self, post: BlogPost) -> Path:
        """Create markdown file for blog post."""
        # Create posts directory if needed
        posts_dir = Path("/opt/gjh-blog-agent/data/posts")
        posts_dir.mkdir(parents=True, exist_ok=True)

        # Create frontmatter
        frontmatter = {
            "title": post.title,
            "slug": post.slug,
            "excerpt": post.excerpt,
            "date": post.created_at.isoformat(),
            "keywords": post.seo_keywords,
            "description": post.meta_description
        }

        # Create file content
        content = f"""---
{json.dumps(frontmatter, indent=2)}
---

{post.content}
"""

        # Write file
        file_path = posts_dir / f"{post.slug}.md"
        file_path.write_text(content)

        return file_path

    def schedule_post(self, db: Session, post: BlogPost, scheduled_for: datetime) -> bool:
        """Schedule a post for future publication."""
        try:
            post.status = "scheduled"
            post.scheduled_for = scheduled_for
            db.commit()

            print(f"✓ Scheduled: {post.title} for {scheduled_for}")
            return True

        except Exception as e:
            print(f"✗ Scheduling failed: {e}")
            return False

    def publish_scheduled_posts(self, db: Session):
        """Publish posts that are scheduled for now or earlier."""
        now = datetime.utcnow()

        scheduled_posts = db.query(BlogPost)\
            .filter(BlogPost.status == "scheduled")\
            .filter(BlogPost.scheduled_for <= now)\
            .all()

        for post in scheduled_posts:
            self.publish_post(db, post)

    def unpublish_post(self, db: Session, post: BlogPost) -> bool:
        """Unpublish a blog post."""
        try:
            post.status = "draft"
            post.deployed = False
            db.commit()

            print(f"✓ Unpublished: {post.title}")
            return True

        except Exception as e:
            print(f"✗ Unpublishing failed: {e}")
            return False

    def get_deployment_status(self, post: BlogPost) -> dict:
        """Get deployment status for a post."""
        return {
            "post_id": post.id,
            "title": post.title,
            "status": post.status,
            "deployed": post.deployed,
            "url": post.vercel_url,
            "published_at": post.published_at.isoformat() if post.published_at else None
        }
