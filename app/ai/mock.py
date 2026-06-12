from app.ai.base import BaseAIClient


class MockAIClient(BaseAIClient):
    async def generate_response(self, message: list[dict]) -> str:
        last_user_message = message[-1]["content"]

        return f"Mock AI response: {last_user_message}"