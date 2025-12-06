from celery import shared_task
from pathlib import Path
import re

@shared_task(bind=True)
def integrate_affiliates_task(self, limit: int = 0):
    """Integrate affiliates into frontend posts asynchronously.
    If limit>0, process only that many posts.
    """
    from utils.blog_affiliate_integration import BlogAffiliateIntegration
    integrator = BlogAffiliateIntegration()

    posts = sorted(Path('frontend/posts').glob('*.md'))
    processed = 0
    modified = []

    for p in posts:
        if limit and processed >= limit:
            break

        text = p.read_text()
        if re.search(r"partnerstack|impact\.com|try\.|utm_source|affiliate", text, re.I):
            continue

        try:
            result = integrator.enhance_post(title=p.stem.replace('-', ' ').title(), content=text, slug=p.stem)
            if result.get('affiliate_count', 0) > 0:
                p.write_text(result['content'])
                modified.append((str(p), result.get('affiliate_count', 0)))
        except Exception as e:
            # Log and continue
            print(f"Error enhancing {p}: {e}")

        processed += 1

    return {'modified': modified, 'processed': processed}
