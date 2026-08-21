"""NVIDIA API client for LLM interactions.

Drop-in replacement for the old Ollama client. Uses the OpenAI-compatible
endpoint at integrate.api.nvidia.com.
"""
import os
import warnings
from typing import List, Dict, Optional

from openai import OpenAI
from config import settings


class NvidiaClient:
    """Client for interacting with NVIDIA API LLM endpoints."""

    def __init__(self, base_url: str = None, model: str = None):
        """Initialize NVIDIA client.

        Args:
            base_url: Override the base URL. Defaults to settings.nvidia_api_base.
            model: Override the model name. Defaults to settings.nvidia_model.
        """
        self.base_url = base_url or settings.nvidia_api_base
        self.model = model or settings.nvidia_model
        self.api_key = settings.nvidia_api_key
        if not self.api_key:
            raise ValueError(
                "NVIDIA_API_KEY is required. Set it in .env"
            )
        self.client = OpenAI(
            base_url=self.base_url,
            api_key=self.api_key,
        )
        # Suppress httpx SSL cert warnings for the free endpoint
        warnings.filterwarnings("ignore", message=".*Certificate has no.*")

    def generate(self, prompt: str, system: str = None, temperature: float = 0.7) -> str:
        """Generate text completion."""
        messages = []

        if system:
            messages.append({"role": "system", "content": system})

        messages.append({"role": "user", "content": prompt})

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            max_tokens=2048,
        )

        return response.choices[0].message.content

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
        # NVIDIA free-tier text-embedding endpoint
        response = self.client.embeddings.create(
            model="nvidia/nv-embed-v1",
            input=text,
        )
        return response.data[0].embedding

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
