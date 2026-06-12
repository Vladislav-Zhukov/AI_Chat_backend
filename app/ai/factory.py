from app.ai.base import BaseAIClient
from app.ai.gemini import GeminiClient
from app.ai.mock import MockAIClient
from app.ai.openai_client import OpenAIClient
from app.core.config import settings


def get_ai_client() -> BaseAIClient:
    if settings.AI_PROVIDER == "mock":
        return MockAIClient()

    if settings.AI_PROVIDER == "openai":
        return OpenAIClient()

    if settings.AI_PROVIDER == "gemini":
        return GeminiClient()

    raise ValueError(f"Unsupported AI provider: {settings.AI_PROVIDER}")

ai_client = get_ai_client()