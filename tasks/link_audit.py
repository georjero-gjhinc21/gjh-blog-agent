from .celery_app import celery_app
from pathlib import Path

@celery_app.task(
    name="tasks.link_audit.weekly_link_audit_task",
    autoretry_for=(Exception,),
    retry_kwargs={"max_retries": 3},
    retry_backoff=True,
    retry_backoff_max=600,
    retry_jitter=True,
)
def weekly_link_audit_task():
    """Run a full-site link audit with closed-loop healing.

    1. Validate links in every post.
    2. Auto-apply known fixes (utils.link_fixer.LINK_FIXES) to posts
       containing broken URLs.
    3. Re-validate fixed posts; write only the *remaining* broken links
       (ones needing new mappings) to broken_links.txt for review.

    Unexpected errors propagate so Celery retries with backoff.
    """
    print("Starting weekly link audit...")
    from utils import link_fixer

    posts = sorted(Path('frontend/posts').glob('*.md'))
    fixed_total = 0
    remaining_all = []
    for p in posts:
        broken = link_fixer.validate_links_in_post(str(p))
        if not broken:
            continue
        fixed = link_fixer.fix_links_in_post(str(p))
        fixed_total += fixed
        if fixed:
            # Re-validate: only still-broken links need human attention.
            broken = link_fixer.validate_links_in_post(str(p))
        for u, code in broken:
            remaining_all.append((u, code, str(p)))

    out = Path('broken_links.txt')
    if remaining_all:
        with out.open('w') as f:
            for u, code, file in remaining_all:
                f.write(f"{code} {u} in file: {file}\n")
    else:
        out.write_text('')

    print(f"Weekly audit complete. Auto-fixed: {fixed_total}, "
          f"remaining broken: {len(remaining_all)}")
    return {"fixed_count": fixed_total, "broken_count": len(remaining_all)}
