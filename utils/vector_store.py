"""Milvus vector store for semantic search."""
try:
    from pymilvus import connections, Collection, CollectionSchema, FieldSchema, DataType, utility
    MILVUS_AVAILABLE = True
except ImportError:
    MILVUS_AVAILABLE = False
    print("Warning: pymilvus not installed. Vector store functionality disabled.")

from typing import List, Dict, Tuple
from config import settings


class VectorStore:
    """Milvus vector store for blog topics and content."""

    def __init__(self):
        """Initialize Milvus connection."""
        if not MILVUS_AVAILABLE:
            self.enabled = False
            return

        try:
            connections.connect(
                alias="default",
                host=settings.milvus_host,
                port=settings.milvus_port
            )
            self.collection_name = settings.milvus_collection_name
            self._ensure_collection()
            self.enabled = True
        except Exception as e:
            print(f"Warning: Could not connect to Milvus: {e}")
            self.enabled = False

    def _ensure_collection(self):
        """Create collection if it doesn't exist."""
        if utility.has_collection(self.collection_name):
            self.collection = Collection(self.collection_name)
        else:
            # Define schema
            fields = [
                FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
                FieldSchema(name="topic_id", dtype=DataType.INT64),
                FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=4096),
                FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=5000),
            ]
            schema = CollectionSchema(fields=fields, description="Blog topics embeddings")

            # Create collection
            self.collection = Collection(self.collection_name, schema)

            # Create index
            index_params = {
                "metric_type": "L2",
                "index_type": "IVF_FLAT",
                "params": {"nlist": 128}
            }
            self.collection.create_index("embedding", index_params)

    def add_topic(self, topic_id: int, text: str, embedding: List[float]):
        """Add a topic embedding to the vector store."""
        if not self.enabled:
            return

        data = [
            [topic_id],
            [embedding],
            [text[:5000]]  # Truncate if needed
        ]
        self.collection.insert(data)
        self.collection.load()

    def search_similar_topics(
        self,
        query_embedding: List[float],
        top_k: int = 5
    ) -> List[Tuple[int, float]]:
        """Search for similar topics."""
        if not self.enabled:
            return []

        self.collection.load()

        search_params = {"metric_type": "L2", "params": {"nprobe": 10}}
        results = self.collection.search(
            data=[query_embedding],
            anns_field="embedding",
            param=search_params,
            limit=top_k,
            output_fields=["topic_id"]
        )

        # Return topic IDs and scores
        similar_topics = []
        for hits in results:
            for hit in hits:
                similar_topics.append((hit.entity.get("topic_id"), hit.distance))

        return similar_topics

    def delete_topic(self, topic_id: int):
        """Delete a topic from vector store."""
        expr = f"topic_id == {topic_id}"
        self.collection.delete(expr)

    def close(self):
        """Close Milvus connection."""
        connections.disconnect("default")
