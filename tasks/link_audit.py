from .celery_app import celery_app
from pathlib import Path

@celery_app.task(name="tasks.link_audit.weekly_link_audit_task")
def weekly_link_audit_task():
    """Run a full-site link audit and write broken_links.txt for review."""
    print("Starting weekly link audit...")
    try:
        from utils import link_fixer

        posts = sorted(Path('frontend/posts').glob('*.md'))
        broken_all = []
        for p in posts:
            broken = link_fixer.validate_links_in_post(str(p))
            if broken:
                for u, code in broken:
                    broken_all.append((u, code, str(p)))

        out = Path('broken_links.txt')
        if broken_all:
            with out.open('w') as f:
                for u, code, file in broken_all:
                    f.write(f"{code} {u} in file: {file}\n")
        else:
            out.write_text('')

        print(f"Weekly audit complete. Broken links: {len(broken_all)}")
        return {"broken_count": len(broken_all)}
    except Exception as e:
        print(f"Link audit failed: {e}")
        return {"error": str(e)}
