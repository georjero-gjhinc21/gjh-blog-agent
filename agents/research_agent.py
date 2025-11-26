"""Research Agent - Discovers trending topics in government contracting."""
import feedparser
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from typing import List, Dict
from sqlalchemy.orm import Session

from models.blog import Topic
from utils.ollama_client import OllamaClient
from utils.vector_store import VectorStore
from config import settings


class ResearchAgent:
    """Discovers and evaluates trending topics for blog posts."""

    def __init__(self):
        """Initialize Research Agent."""
        self.ollama = OllamaClient()
        self.vector_store = VectorStore()
        self.focus_topics = settings.focus_topics
        self.sources = settings.research_sources

    def discover_topics(self, db: Session, max_topics: int = 10) -> List[Topic]:
        """Discover new trending topics from RSS feeds and sources."""
        discovered_topics = []

        # 1. Fetch from RSS feeds
        for source_url in self.sources:
            try:
                feed = feedparser.parse(source_url)
                for entry in feed.entries[:5]:  # Top 5 from each feed
                    # Check if already exists
                    existing = db.query(Topic).filter_by(source_url=entry.link).first()
                    if existing:
                        continue

                    # Analyze relevance
                    relevance_score = self._analyze_relevance(entry.title, entry.get("summary", ""))

                    if relevance_score > 0.6:  # Threshold for relevance
                        topic = self._create_topic(entry, relevance_score, db)
                        discovered_topics.append(topic)

            except Exception as e:
                print(f"Error fetching from {source_url}: {e}")
                continue

        # 2. Generate synthetic trending topics based on focus areas
        synthetic_topics = self._generate_synthetic_topics(db, count=3)
        discovered_topics.extend(synthetic_topics)

        # Sort by trend score
        discovered_topics.sort(key=lambda x: x.trend_score, reverse=True)

        return discovered_topics[:max_topics]

    def _analyze_relevance(self, title: str, summary: str) -> float:
        """Analyze how relevant a topic is to our focus areas."""
        text = f"{title}\n{summary}"

        system = """You are a relevance analyzer for a government contracting and technology consulting blog.
Focus areas: government contracting, federal procurement, GSA schedules, SBIR/STTR grants,
technology consulting, data analytics, cybersecurity compliance."""

        prompt = f"""Analyze the relevance of this article to our blog focus areas.
Return ONLY a number between 0.0 and 1.0, where:
- 0.0 = completely irrelevant
- 0.5 = somewhat relevant
- 1.0 = highly relevant

Article:
{text}

Relevance score:"""

        try:
            response = self.ollama.generate(prompt, system, temperature=0.3)
            score = float(response.strip())
            return max(0.0, min(1.0, score))
        except:
            # Fallback: keyword matching
            score = 0.0
            for topic in self.focus_topics:
                if topic.lower() in text.lower():
                    score += 0.2
            return min(1.0, score)

    def _create_topic(self, entry: Dict, score: float, db: Session) -> Topic:
        """Create a Topic object from feed entry."""
        title = entry.get("title", "")
        summary = entry.get("summary", "")

        # Extract keywords
        keywords = self.ollama.extract_keywords(f"{title}\n{summary}", max_keywords=10)

        # Create topic
        topic = Topic(
            title=title,
            description=summary[:1000],
            source_url=entry.get("link", ""),
            trend_score=score,
            keywords=keywords,
            created_at=datetime.utcnow(),
            used=False
        )

        db.add(topic)
        db.commit()
        db.refresh(topic)

        # Add to vector store
        try:
            embedding = self.ollama.embed(f"{title}\n{summary}")
            self.vector_store.add_topic(topic.id, f"{title}\n{summary}", embedding)
        except Exception as e:
            print(f"Error adding to vector store: {e}")

        return topic

    def _generate_synthetic_topics(self, db: Session, count: int = 3) -> List[Topic]:
        """Generate synthetic trending topics based on focus areas."""
        synthetic_topics = []

        system = """You are a government contracting and technology consulting expert.
Generate timely, relevant blog topic ideas that would interest government contractors and federal agencies."""

        prompt = f"""Generate {count} timely blog post topic ideas for {datetime.now().strftime('%B %Y')}.

Focus areas:
{chr(10).join(f"- {topic}" for topic in self.focus_topics)}

For each topic, provide:
1. A compelling title (max 100 characters)
2. A brief description (2-3 sentences)

Format each as:
TITLE: [title]
DESCRIPTION: [description]
---"""

        try:
            response = self.ollama.generate(prompt, system, temperature=0.8)

            # Parse response
            topic_blocks = response.split("---")
            for block in topic_blocks:
                if "TITLE:" in block and "DESCRIPTION:" in block:
                    try:
                        title_line = [l for l in block.split("\n") if "TITLE:" in l][0]
                        desc_line = [l for l in block.split("\n") if "DESCRIPTION:" in l][0]

                        title = title_line.split("TITLE:")[1].strip()
                        description = desc_line.split("DESCRIPTION:")[1].strip()

                        # Check if similar topic exists
                        title_embedding = self.ollama.embed(title)
                        similar = self.vector_store.search_similar_topics(title_embedding, top_k=1)

                        if not similar or similar[0][1] > 0.5:  # Not too similar
                            keywords = self.ollama.extract_keywords(f"{title}\n{description}", max_keywords=8)

                            topic = Topic(
                                title=title,
                                description=description,
                                source_url="",
                                trend_score=0.7,  # Synthetic topics get good score
                                keywords=keywords,
                                created_at=datetime.utcnow(),
                                used=False
                            )

                            db.add(topic)
                            db.commit()
                            db.refresh(topic)

                            # Add to vector store
                            self.vector_store.add_topic(topic.id, f"{title}\n{description}", title_embedding)

                            synthetic_topics.append(topic)

                            if len(synthetic_topics) >= count:
                                break
                    except Exception as e:
                        print(f"Error parsing topic block: {e}")
                        continue

        except Exception as e:
            print(f"Error generating synthetic topics: {e}")

        return synthetic_topics

    def get_unused_topic(self, db: Session) -> Topic:
        """Get the highest-scored unused topic."""
        topic = db.query(Topic)\
            .filter_by(used=False)\
            .order_by(Topic.trend_score.desc())\
            .first()

        if topic:
            return topic

        # If no unused topics, discover new ones
        new_topics = self.discover_topics(db, max_topics=5)
        return new_topics[0] if new_topics else None

    def mark_topic_used(self, db: Session, topic_id: int):
        """Mark a topic as used."""
        topic = db.query(Topic).filter_by(id=topic_id).first()
        if topic:
            topic.used = True
            db.commit()
