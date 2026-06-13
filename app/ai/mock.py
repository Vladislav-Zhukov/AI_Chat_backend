import asyncio
from collections.abc import AsyncGenerator

from app.ai.base import BaseAIClient


class MockAIClient(BaseAIClient):
    async def generate_response(self, messages: list[dict]) -> str:
        user_messages = [
            message["content"]
            for message in messages
            if message["role"] == "user"
        ]

        last_user_message = user_messages[-1] if user_messages else ""

        return f"Mock AI response: {last_user_message}"

    async def stream_response(self, messages: list[dict]) -> AsyncGenerator[str, None]:
        full_response = await self.generate_response(messages)

        for word in full_response.split():
            await asyncio.sleep(0.2)
            yield word + " "