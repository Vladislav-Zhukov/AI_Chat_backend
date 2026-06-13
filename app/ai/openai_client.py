from app.ai.base import BaseAIClient
from collections.abc import AsyncGenerator


class OpenAIClient(BaseAIClient):
    async def generate_response(self, message: list[dict]) -> str:
        raise NotImplementedError("OpenAI provider is not implemented yet")

    async def stream_response(self, messages: list[dict]) -> AsyncGenerator[str, None]:
        raise NotImplementedError("Streaming is not implemented yet")
