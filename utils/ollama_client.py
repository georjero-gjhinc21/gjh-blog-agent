"""Ollama client for local LLM interactions."""
import ollama
from typing import List, Dict, Optional
from config import settings


class OllamaClient:
    """Client for interacting with local Ollama instance."""

    def __init__(self, host: str = None, model: str = None):
        """Initialize Ollama client."""
        self.host = host or settings.ollama_host
        self.model = model or settings.ollama_model
        self.client = ollama.Client(host=self.host)

    def generate(self, prompt: str, system: str = None, temperature: float = 0.7) -> str:
        """Generate text completion."""
        messages = []

        if system:
            messages.append({"role": "system", "content": system})

        messages.append({"role": "user", "content": prompt})

        response = self.client.chat(
            model=self.model,
            messages=messages,
            options={"temperature": temperature}
        )

        return response["message"]["content"]

    def generate_with_context(
        self,
        prompt: str,
        context: List[str],
        system: str = None,
        temperature: float = 0.7
    ) -> str:
        """Generate text with additional context."""
        context_str = "\n\n".join(context)
        full_prompt = f"Context:\n{context_str}\n\nTask:\n{prompt}"

        return self.generate(full_prompt, system, temperature)

    def embed(self, text: str) -> List[float]:
        """Generate embeddings for text."""
        response = self.client.embeddings(
            model=self.model,
            prompt=text
        )
        return response["embedding"]

    def extract_keywords(self, text: str, max_keywords: int = 10) -> List[str]:
        """Extract keywords from text."""
        system = "You are a keyword extraction expert. Extract the most important keywords from the given text."
        prompt = f"Extract up to {max_keywords} keywords from this text. Return only the keywords as a comma-separated list:\n\n{text}"

        response = self.generate(prompt, system, temperature=0.3)
        keywords = [k.strip() for k in response.split(",")]
        return keywords[:max_keywords]

    def summarize(self, text: str, max_length: int = 200) -> str:
        """Summarize text."""
        system = "You are a professional summarizer. Create concise, informative summaries."
        prompt = f"Summarize the following text in approximately {max_length} characters:\n\n{text}"

        return self.generate(prompt, system, temperature=0.5)
