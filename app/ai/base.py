from abc import ABC, abstractmethod
from collections.abc import AsyncGenerator


class BaseAIClient(ABC):
    @abstractmethod
    async def generate_response(self, message: list[dict]) -> str:
        pass

    @abstractmethod
    async def stream_response(self, message: list[dict]) -> AsyncGenerator[str, None]:
        pass