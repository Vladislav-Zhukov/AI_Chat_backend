from app.ai.base import BaseAIClient


class GeminiClient(BaseAIClient):
    async def generate_response(self, message: list[dict]) -> str:
        raise NotImplementedError("Gemini provider is not implemented yet")