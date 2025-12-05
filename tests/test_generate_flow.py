import sys
import types
from datetime import datetime

# Prepare fake modules before importing main
fake_db_module = types.ModuleType('database')

class FakeSessionCM:
    def __enter__(self):
        return {}
    def __exit__(self, exc_type, exc, tb):
        return False

def fake_init_db():
    return None

fake_db_module.get_db_session = FakeSessionCM
fake_db_module.init_db = fake_init_db

# Fake models.blog
fake_models_blog = types.ModuleType('models.blog')
class FakeBlogPost:
    def __init__(self):
        self.id = 1
        self.title = 'Test Title'
        self.slug = 'test-title'
        self.word_count = 900
        self.status = 'draft'
        self.excerpt = 'An excerpt.'
        self.seo_keywords = ['ai','govcon']
        self.metadata = {'affiliate_matches': [{'name':'P','network':'partnerstack','score':0.95}]}
        self.created_at = datetime.now()
        self.vercel_url = 'https://example.com/test-title'

fake_models_blog.BlogPost = FakeBlogPost

# Fake agents package and unified agent
fake_agents = types.ModuleType('agents')

class ResearchAgent:
    def discover_topics(self, db, max_topics=10):
        return []
    def get_unused_topic(self, db):
        topic = types.SimpleNamespace(id=42, title='AI in GovCon', keywords=['ai','govcon'])
        return topic
    def mark_topic_used(self, db, topic_id):
        return None

class AffiliateAgent:
    def seed_sample_products(self, db):
        return None
    def match_product_to_topic(self, db, topic):
        return None

class ContentAgent:
    def __init__(self, unified_affiliate_agent=None):
        self.unified = unified_affiliate_agent
    def generate_post(self, db, topic, use_unified_affiliates=False, max_affiliate_matches=3, affiliate_product=None):
        return FakeBlogPost()

class PublishingAgent:
    def publish_post(self, db, post):
        post.vercel_url = 'https://example.com/published'
        post.status = 'published'
        return True

class MonitoringAgent:
    def get_performance_summary(self, db, days=30):
        return {'total_posts':1,'total_views':1000,'total_affiliate_clicks':10,'total_revenue':50.0,'avg_views_per_post':1000.0,'avg_revenue_per_post':50.0,'click_through_rate':1.0}
    def get_top_performing_posts(self, db, limit=5):
        return []
    def get_top_revenue_posts(self, db, limit=5):
        return []

fake_agents.ResearchAgent = ResearchAgent
fake_agents.AffiliateAgent = AffiliateAgent
fake_agents.ContentAgent = ContentAgent
fake_agents.PublishingAgent = PublishingAgent
fake_agents.MonitoringAgent = MonitoringAgent

# Fake unified_affiliate_agent module
fake_unified = types.ModuleType('agents.unified_affiliate_agent')
class UnifiedAffiliateAgent:
    def sync_all_programs(self):
        return {'partnerstack': 1, 'impact': 0, 'total': 1}
    def get_stats(self):
        return {'networks': {'partnerstack':1,'impact':0,'total':1}, 'categories': {}, 'top_commission_programs': []}
    def test_connections(self):
        return {'partnerstack': True, 'impact': True}
    def search_programs(self, query, limit):
        return []
    def find_best_matches(self, content, title, max_matches=3):
        return [{'name':'P','network':'partnerstack','match_score':0.9,'commission_rate':10.0}]
    def generate_link(self, program_name, sub_id=None):
        return 'https://affiliate.example.com'

fake_unified.UnifiedAffiliateAgent = UnifiedAffiliateAgent

# Inject into sys.modules
sys.modules['database'] = fake_db_module
# Provide a 'models' package and its 'blog' submodule
models_pkg = types.ModuleType('models')
models_pkg.blog = fake_models_blog
sys.modules['models'] = models_pkg
sys.modules['models.blog'] = fake_models_blog
sys.modules['agents'] = fake_agents
sys.modules['agents.unified_affiliate_agent'] = fake_unified

# Now import main (it will use the fake modules)
import importlib.util
import importlib.machinery
import os

# Load main.py directly
main_path = os.path.join(os.path.dirname(__file__), '..', 'main.py')
loader = importlib.machinery.SourceFileLoader('main', main_path)
spec = importlib.util.spec_from_loader(loader.name, loader)
main = importlib.util.module_from_spec(spec)
loader.exec_module(main)


def test_generate_flow_executes():
    # Call generate - should run without raising
    main.generate()
    # No explicit asserts; success is no exception
