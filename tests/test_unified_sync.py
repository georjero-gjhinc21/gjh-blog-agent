import sys
import types
import importlib.util
import importlib.machinery
import importlib
import os

# Minimal fakes for main imports
fake_db = types.ModuleType('database')
class SessionCM:
    def __enter__(self):
        return {}
    def __exit__(self, exc_type, exc, tb):
        return False
fake_db.get_db_session = SessionCM
fake_db.init_db = lambda: None
sys.modules['database'] = fake_db

models_pkg = types.ModuleType('models')
blog_mod = types.ModuleType('models.blog')
class BlogPost:
    pass
blog_mod.BlogPost = BlogPost
models_pkg.blog = blog_mod
sys.modules['models'] = models_pkg
sys.modules['models.blog'] = blog_mod

# Ensure agents package exists for imports
fake_agents_pkg = types.ModuleType('agents')
class ResearchAgent: pass
class AffiliateAgent: pass
class ContentAgent: pass
class PublishingAgent: pass
class MonitoringAgent: pass
fake_agents_pkg.ResearchAgent = ResearchAgent
fake_agents_pkg.AffiliateAgent = AffiliateAgent
fake_agents_pkg.ContentAgent = ContentAgent
fake_agents_pkg.PublishingAgent = PublishingAgent
fake_agents_pkg.MonitoringAgent = MonitoringAgent
sys.modules['agents'] = fake_agents_pkg


def _load_main():
    main_path = os.path.join(os.path.dirname(__file__), '..', 'main.py')
    loader = importlib.machinery.SourceFileLoader('main', main_path)
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


def test_sync_unified_success():
    fake_unified = types.ModuleType('agents.unified_affiliate_agent')
    class UnifiedAffiliateAgent:
        def sync_all_programs(self):
            return {'partnerstack': 5, 'impact': 3, 'total': 8}
    fake_unified.UnifiedAffiliateAgent = UnifiedAffiliateAgent
    sys.modules['agents.unified_affiliate_agent'] = fake_unified

    # load/reload main so it picks up the fake
    main = _load_main()

    # Should not raise
    main.sync_unified()


def test_sync_unified_network_error():
    fake_unified = types.ModuleType('agents.unified_affiliate_agent')
    class UnifiedAffiliateAgent:
        def sync_all_programs(self):
            raise Exception('network failure')
    fake_unified.UnifiedAffiliateAgent = UnifiedAffiliateAgent
    sys.modules['agents.unified_affiliate_agent'] = fake_unified

    main = _load_main()

    # sync_unified handles exceptions internally; should not raise
    main.sync_unified()
