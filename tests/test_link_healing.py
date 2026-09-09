"""Closed-loop link healing tests (no infra required).

Uses a tmp cwd with fixture posts and a stubbed requests.head so no
network or broker is touched. The Celery task body runs synchronously
via Task.run().
"""
from pathlib import Path

from utils import link_fixer
from tasks.link_audit import weekly_link_audit_task
from tasks import blog_tasks, integrate_affiliates

KNOWN_BROKEN = "https://www.wati.io/pricing/"
KNOWN_FIXED = "https://affiliates.wati.io/mq5gz7zpyn9a"
UNKNOWN_BROKEN = "https://example.invalid/dead-page"

CODES = {KNOWN_BROKEN: 404, KNOWN_FIXED: 200, UNKNOWN_BROKEN: 404}


class _Resp:
    def __init__(self, code):
        self.status_code = code


def _fake_head(url, **kwargs):
    return _Resp(CODES.get(url, 200))


def _make_post(tmp_path):
    posts = tmp_path / "frontend" / "posts"
    posts.mkdir(parents=True)
    post = posts / "fixture-post.md"
    post.write_text(
        f"# Fixture\n\nSee {KNOWN_BROKEN} and {UNKNOWN_BROKEN}\n")
    return post


def test_fixer_replaces_known_broken_url(tmp_path, monkeypatch):
    post = _make_post(tmp_path)
    monkeypatch.chdir(tmp_path)
    fixed = link_fixer.fix_links_in_post(str(post))
    assert fixed == 1
    content = post.read_text()
    assert KNOWN_FIXED in content
    assert KNOWN_BROKEN not in content


def test_audit_closed_loop_fixes_and_reports_remainder(
        tmp_path, monkeypatch):
    post = _make_post(tmp_path)
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(link_fixer.requests, "head", _fake_head)

    result = weekly_link_audit_task.run()

    assert result["fixed_count"] == 1
    assert result["broken_count"] == 1
    assert KNOWN_FIXED in post.read_text()
    report = (tmp_path / "broken_links.txt").read_text()
    assert UNKNOWN_BROKEN in report
    assert "wati.io/pricing" not in report


def test_tasks_have_autoretry_with_backoff():
    tasks = [
        weekly_link_audit_task,
        blog_tasks.discover_topics_task,
        blog_tasks.generate_blog_post_task,
        blog_tasks.publish_scheduled_posts_task,
        blog_tasks.update_metrics_task,
        integrate_affiliates.integrate_affiliates_task,
    ]
    for task in tasks:
        assert task.autoretry_for == (Exception,), task.name
        assert task.retry_kwargs.get("max_retries", 0) >= 2, task.name
        assert task.retry_backoff is True, task.name
    # Generate task is capped lower: not fully idempotent (extra drafts).
    assert blog_tasks.generate_blog_post_task.retry_kwargs[
        "max_retries"] == 2
