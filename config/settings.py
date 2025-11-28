"""Application configuration settings."""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Database
    database_url: str = "postgresql://gjh_admin:gjh_secure_password_2024@localhost:5432/gjh_blog"

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    # Milvus
    milvus_host: str = "localhost"
    milvus_port: int = 19530
    milvus_collection_name: str = "blog_topics"

    # Ollama
    ollama_host: str = "http://localhost:11434"
    ollama_model: str = "llama3.1:8b"

    # Blog settings
    blog_domain: str = "gjhconsulting.net"
    posts_per_week: int = 3
    min_words: int = 800
    max_words: int = 1500

    # Focus topics
    focus_topics: List[str] = [
        "government contracting",
        "federal procurement",
        "GSA schedules",
        "SBIR/STTR grants",
        "technology consulting",
        "data analytics",
        "cybersecurity compliance"
    ]

    # Research settings
    research_sources: List[str] = [
        "https://www.govcon.com/feed/",
        "https://www.federalnewsnetwork.com/category/contracting/feed/",
        "https://www.govtech.com/rss",
    ]

    # PartnerStack
    partnerstack_api_key: str = ""
    partnerstack_partner_key: str = ""

    # Impact.com
    impact_account_sid: str = ""
    impact_auth_token: str = ""

    # Vercel
    vercel_token: str = ""
    vercel_project_id: str = ""

    class Config:
        env_file = ".env"
        extra = "allow"


settings = Settings()
