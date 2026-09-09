"""Portable posts directory resolution tests (no infra required)."""
import importlib.machinery
import importlib.util
import sys
import types
from datetime import datetime
from pathlib import Path
from types import SimpleNamespace


def _load_publishing_module():
    """Load agents/publishing_agent.py without importing the agents package."""
    # Stub heavy third-party/project imports so this test needs only stdlib.
    if "sqlalchemy" not in sys.modules:
        sqlalchemy_mod = types.ModuleType("sqlalchemy")
        orm_mod = types.ModuleType("sqlalchemy.orm")
        orm_mod.Session = object  # type: ignore[attr-defined]
        sqlalchemy_mod.orm = orm_mod  # type: ignore[attr-defined]
        sys.modules["sqlalchemy"] = sqlalchemy_mod
        sys.modules["sqlalchemy.orm"] = orm_mod
    if "sqlalchemy.orm" not in sys.modules:
        orm_mod = types.ModuleType("sqlalchemy.orm")
        orm_mod.Session = object  # type: ignore[attr-defined]
        sys.modules["sqlalchemy.orm"] = orm_mod

    if "models.blog" not in sys.modules:
        models_pkg = sys.modules.get("models") or types.ModuleType("models")
        sys.modules["models"] = models_pkg
        blog_mod = types.ModuleType("models.blog")

        class BlogPost:  # minimal stand-in; only used for typing
            pass

        blog_mod.BlogPost = BlogPost  # type: ignore[attr-defined]
        sys.modules["models.blog"] = blog_mod
        models_pkg.blog = blog_mod  # type: ignore[attr-defined]

    if "config" not in sys.modules:
        config_mod = types.ModuleType("config")
        config_mod.settings = SimpleNamespace(  # type: ignore[attr-defined]
            vercel_token="",
            vercel_project_id="",
            blog_domain="example.com",
        )
        sys.modules["config"] = config_mod

    path = Path(__file__).resolve().parent.parent / "agents" / "publishing_agent.py"
    loader = importlib.machinery.SourceFileLoader("publishing_agent_under_test", str(path))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[loader.name] = module
    loader.exec_module(module)
    return module


_mod = _load_publishing_module()

REPO_ROOT = _mod.REPO_ROOT
DEFAULT_POSTS_DIR = _mod.DEFAULT_POSTS_DIR
_resolve_posts_dir = _mod._resolve_posts_dir
PublishingAgent = _mod.PublishingAgent


def test_default_resolves_to_repo_frontend_posts(monkeypatch):
    monkeypatch.delenv("POSTS_DIR", raising=False)
    assert _resolve_posts_dir() == REPO_ROOT / "frontend" / "posts"
    assert DEFAULT_POSTS_DIR == REPO_ROOT / "frontend" / "posts"


def test_absolute_posts_dir_override_is_honored(monkeypatch, tmp_path):
    monkeypatch.setenv("POSTS_DIR", str(tmp_path))
    assert _resolve_posts_dir() == tmp_path


def test_relative_posts_dir_is_anchored_to_repo_root(monkeypatch):
    monkeypatch.setenv("POSTS_DIR", "custom/posts")
    assert _resolve_posts_dir() == REPO_ROOT / "custom" / "posts"


def test_create_post_file_writes_only_to_override_dir(monkeypatch, tmp_path):
    monkeypatch.setenv("POSTS_DIR", str(tmp_path))
    agent = PublishingAgent()
    post = SimpleNamespace(
        title="Test Post",
        slug="test-portable-posts-dir",
        excerpt="Excerpt",
        created_at=datetime(2026, 1, 1),
        seo_keywords=["govcon"],
        meta_description="Description",
        content="Hello world",
        affiliate_product=None,
    )
    out = agent._create_post_file(post)
    assert out == tmp_path / "test-portable-posts-dir.md"
    assert out.exists()
    # Real checkout directory must remain untouched by this test.
    assert (REPO_ROOT / "frontend" / "posts" / "test-portable-posts-dir.md").exists() is False
