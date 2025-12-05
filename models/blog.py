"""Database models for blog system."""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Boolean, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Topic(Base):
    """Trending topics discovered by Research Agent."""
    __tablename__ = "topics"

    id = Column(Integer, primary_key=True)
    title = Column(String(500), nullable=False)
    description = Column(Text)
    source_url = Column(String(1000))
    trend_score = Column(Float, default=0.0)
    keywords = Column(JSON)  # List of keywords
    created_at = Column(DateTime, default=datetime.utcnow)
    used = Column(Boolean, default=False)

    # Relationship
    blog_posts = relationship("BlogPost", back_populates="topic")


class AffiliateProduct(Base):
    """PartnerStack affiliate products."""
    __tablename__ = "affiliate_products"

    id = Column(Integer, primary_key=True)
    name = Column(String(500), nullable=False)
    description = Column(Text)
    category = Column(String(200))
    affiliate_link = Column(String(1000), nullable=False)
    commission_rate = Column(Float)
    relevance_keywords = Column(JSON)  # Keywords for matching
    created_at = Column(DateTime, default=datetime.utcnow)
    active = Column(Boolean, default=True)

    # Relationship
    blog_posts = relationship("BlogPost", back_populates="affiliate_product")


class BlogPost(Base):
    """Generated blog posts."""
    __tablename__ = "blog_posts"

    id = Column(Integer, primary_key=True)
    title = Column(String(500), nullable=False)
    slug = Column(String(500), unique=True, nullable=False)
    content = Column(Text, nullable=False)
    excerpt = Column(Text)
    word_count = Column(Integer)

    # Foreign keys
    topic_id = Column(Integer, ForeignKey("topics.id"))
    affiliate_product_id = Column(Integer, ForeignKey("affiliate_products.id"))

    # Metadata
    seo_keywords = Column(JSON)
    meta_description = Column(String(300))

    # Status
    status = Column(String(50), default="draft")  # draft, published, scheduled
    scheduled_for = Column(DateTime)
    published_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Vercel deployment
    vercel_url = Column(String(1000))
    deployed = Column(Boolean, default=False)

    # Relationships
    topic = relationship("Topic", back_populates="blog_posts")
    affiliate_product = relationship("AffiliateProduct", back_populates="blog_posts")
    metrics = relationship("PostMetrics", back_populates="blog_post", uselist=False)


class PostMetrics(Base):
    """Performance metrics for blog posts."""
    __tablename__ = "post_metrics"

    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey("blog_posts.id"), unique=True)

    # Traffic metrics
    page_views = Column(Integer, default=0)
    unique_visitors = Column(Integer, default=0)
    avg_time_on_page = Column(Float, default=0.0)
    bounce_rate = Column(Float, default=0.0)

    # Affiliate metrics
    affiliate_clicks = Column(Integer, default=0)
    affiliate_conversions = Column(Integer, default=0)
    affiliate_revenue = Column(Float, default=0.0)

    # SEO metrics
    organic_traffic = Column(Integer, default=0)
    search_ranking = Column(JSON)  # {keyword: ranking}

    # Timestamps
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    blog_post = relationship("BlogPost", back_populates="metrics")


class TaskRun(Base):
    """Lightweight record of Celery task runs for observability and idempotency checks."""
    __tablename__ = 'task_runs'

    id = Column(Integer, primary_key=True)
    task_id = Column(String(200), unique=True, nullable=False)
    task_name = Column(String(200), nullable=False)
    status = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
