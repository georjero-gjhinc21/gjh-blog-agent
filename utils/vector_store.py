"""SQLite vector store for topic deduplication.

Drop-in replacement for the old Milvus-based VectorStore. Uses cosine similarity
to deduplicate topics across sessions. No external dependencies needed.
"""
import math
import sqlite3
import os
from typing import List, Tuple, Optional
from config import settings


class VectorStore:
    """SQLite-backed vector store for blog topic deduplication."""

    def __init__(self, db_path: str = None):
        """Initialize SQLite vector store.

        Args:
            db_path: Path to the SQLite database file.
        """
        self.db_path = db_path or os.path.join(
            os.path.dirname(__file__), "..", "data", "topics.db"
        )
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.enabled = True
        self._init_db()

    def _get_conn(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        """Create tables if they don't exist."""
        conn = self._get_conn()
        conn.execute("""
            CREATE TABLE IF NOT EXISTS topics (
                id INTEGER PRIMARY KEY,
                topic_id INTEGER UNIQUE,
                embedding TEXT,
                text TEXT
            )
        """)
        conn.commit()
        conn.close()

    def add_topic(self, topic_id: int, text: str, embedding: List[float]):
        """Add a topic embedding to the store."""
        if not self.enabled:
            return

        conn = self._get_conn()
        try:
            conn.execute(
                "INSERT OR REPLACE INTO topics (topic_id, embedding, text) VALUES (?, ?, ?)",
                (topic_id, str(embedding), text[:5000])
            )
            conn.commit()
        finally:
            conn.close()

    def search_similar_topics(
        self,
        query_embedding: List[float],
        top_k: int = 5
    ) -> List[Tuple[int, float]]:
        """Search for similar topics using cosine similarity."""
        if not self.enabled:
            return []

        query_vec = _normalize(query_embedding)
        conn = self._get_conn()
        try:
            rows = conn.execute(
                "SELECT topic_id, embedding, text FROM topics"
            ).fetchall()

            if not rows:
                return []

            scores = []
            for row in rows:
                try:
                    stored_vec = _normalize(_parse_embedding(row["embedding"]))
                    sim = _cosine_similarity(query_vec, stored_vec)
                    scores.append((row["topic_id"], 1.0 - sim))  # distance = 1 - similarity
                except Exception:
                    continue

            scores.sort(key=lambda x: x[1])
            return scores[:top_k]
        finally:
            conn.close()

    def delete_topic(self, topic_id: int):
        """Delete a topic from the store."""
        if not self.enabled:
            return
        conn = self._get_conn()
        try:
            conn.execute("DELETE FROM topics WHERE topic_id = ?", (topic_id,))
            conn.commit()
        finally:
            conn.close()

    def close(self):
        """Close connections (SQLite auto-closes, but kept for API compat)."""
        pass


def _parse_embedding(text: str) -> List[float]:
    """Parse a list string back to a list of floats."""
    import ast
    return ast.literal_eval(text)


def _normalize(vec: List[float]) -> List[float]:
    """L2-normalize a vector."""
    norm = math.sqrt(sum(x * x for x in vec))
    if norm == 0:
        return vec
    return [x / norm for x in vec]


def _cosine_similarity(a: List[float], b: List[float]) -> float:
    """Compute cosine similarity between two vectors."""
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)
