import sys
import types
from datetime import datetime

# Fake database context manager
fake_db = types.ModuleType('database')
class QueryMock:
    def __init__(self, items=None):
        self._items = items or []
    def filter_by(self, **kwargs):
        return self
    def order_by(self, *args, **kwargs):
        return self
    def limit(self, n):
        return self
    def all(self):
        return self._items

class FakeDB:
    def __init__(self):
        import types as _types
        self._items = [_types.SimpleNamespace(id=1, name='Fake', category='AI', commission_rate=10.0)]
    def query(self, model):
        return QueryMock(self._items)

class SessionCM:
    def __enter__(self):
        return FakeDB()
    def __exit__(self, exc_type, exc, tb):
        return False
fake_db.get_db_session = SessionCM
fake_db.init_db = lambda: None
sys.modules['database'] = fake_db

# Fake models and agents for list_affiliates
fake_models_blog = types.ModuleType('models.blog')
class AffiliateProduct:
    def __init__(self):
        self.id = 1
        self.name = 'Fake'
        self.category = 'AI'
        self.commission_rate = 10.0

fake_models_blog.AffiliateProduct = AffiliateProduct
# Provide models package
models_pkg = types.ModuleType('models')
models_pkg.blog = fake_models_blog
# Also provide BlogPost to satisfy imports
blog_mod = types.ModuleType('models.blog')
class BlogPost:
    def __init__(self):
        self.id = 1
        self.title = 'Fake'
        self.slug = 'fake'
        self.word_count = 100
        self.status = 'draft'
        self.excerpt = ''
        self.seo_keywords = []
        self.metadata = {}
        self.created_at = None
        self.vercel_url = ''
blog_mod.BlogPost = BlogPost
# Ensure AffiliateProduct is present on the blog_mod used by FakeDB
# Provide attribute placeholders used by main.py (e.g., .name and .commission_rate.desc())
class _Col:
    def desc(self):
        return self
class AffiliateProductClass:
    name = _Col()
    commission_rate = _Col()

blog_mod.AffiliateProduct = AffiliateProductClass
sys.modules['models'] = models_pkg
sys.modules['models.blog'] = blog_mod

fake_agents = types.ModuleType('agents')
class AffiliateAgent:
    def __init__(self): pass
class ResearchAgent:
    def __init__(self): pass
class ContentAgent:
    def __init__(self): pass
class PublishingAgent:
    def __init__(self): pass
class MonitoringAgent:
    def __init__(self): pass

fake_agents.AffiliateAgent = AffiliateAgent
fake_agents.ResearchAgent = ResearchAgent
fake_agents.ContentAgent = ContentAgent
fake_agents.PublishingAgent = PublishingAgent
fake_agents.MonitoringAgent = MonitoringAgent
sys.modules['agents'] = fake_agents

# Load main
import importlib.util, importlib.machinery, os
main_path = os.path.join(os.path.dirname(__file__), '..', 'main.py')
loader = importlib.machinery.SourceFileLoader('main', main_path)
spec = importlib.util.spec_from_loader(loader.name, loader)
main = importlib.util.module_from_spec(spec)
loader.exec_module(main)


def test_list_affiliates_runs_default():
    main.list_affiliates()


def test_list_affiliates_runs_commission():
    main.list_affiliates(sort_by='commission')
