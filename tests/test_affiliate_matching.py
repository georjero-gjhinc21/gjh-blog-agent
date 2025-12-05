import sys
import types

# Fake unified_affiliate_agent
fake_unified = types.ModuleType('agents.unified_affiliate_agent')
class UnifiedAffiliateAgent:
    def find_best_matches(self, content, title, max_matches=3):
        return [{'name':'FakeProgram','network':'partnerstack','match_score':0.88,'commission_rate':12.5}]
    def search_programs(self, query, limit):
        return [{'name':'FakeProgram','category':'AI','commission_rate':12.5}]
    def test_connections(self):
        return {'partnerstack': True, 'impact': True}

fake_unified.UnifiedAffiliateAgent = UnifiedAffiliateAgent

# Inject minimal fake 'database' and 'agents' packages to satisfy main imports
# Fake database
fake_db = types.ModuleType('database')
class SessionCM:
    def __enter__(self):
        return {}
    def __exit__(self, exc_type, exc, tb):
        return False
fake_db.get_db_session = SessionCM
fake_db.init_db = lambda: None
sys.modules['database'] = fake_db

# Fake models package with BlogPost
models_pkg = types.ModuleType('models')
blog_mod = types.ModuleType('models.blog')
class BlogPost:
    def __init__(self):
        self.id = 1
        self.title = 'Fake'
        self.slug = 'fake'
        self.word_count = 1000
        self.status = 'draft'
        self.excerpt = 'x'
        self.seo_keywords = []
        self.metadata = {}
        self.created_at = None
        self.vercel_url = ''
blog_mod.BlogPost = BlogPost
models_pkg.blog = blog_mod
sys.modules['models'] = models_pkg
sys.modules['models.blog'] = blog_mod

# Fake agents with required classes
fake_agents_pkg = types.ModuleType('agents')
class ResearchAgent:
    pass
class AffiliateAgent:
    pass
class ContentAgent:
    pass
class PublishingAgent:
    pass
class MonitoringAgent:
    pass
fake_agents_pkg.ResearchAgent = ResearchAgent
fake_agents_pkg.AffiliateAgent = AffiliateAgent
fake_agents_pkg.ContentAgent = ContentAgent
fake_agents_pkg.PublishingAgent = PublishingAgent
fake_agents_pkg.MonitoringAgent = MonitoringAgent
sys.modules['agents'] = fake_agents_pkg
sys.modules['agents.unified_affiliate_agent'] = fake_unified

# Load main directly
import importlib.util, importlib.machinery, os
main_path = os.path.join(os.path.dirname(__file__), '..', 'main.py')
loader = importlib.machinery.SourceFileLoader('main', main_path)
spec = importlib.util.spec_from_loader(loader.name, loader)
main = importlib.util.module_from_spec(spec)
loader.exec_module(main)


def test_match_content_runs():
    # Should run without error and print table
    main.match_content('AI tools', max_matches=1)


def test_search_unified_runs():
    main.search_unified('AI', limit=1)
