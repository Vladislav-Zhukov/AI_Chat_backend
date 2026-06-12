from app.ai.base import BaseAIClient


class OpenAIClient(BaseAIClient):
    async def generate_response(self, message: list[dict]) -> str:
        raise NotImplementedError("OpenAI provider is not implemented yet")