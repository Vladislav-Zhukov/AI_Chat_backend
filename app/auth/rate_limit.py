from fastapi import HTTPException, status

from app.core.config import settings
from app.core.redis import redis_client
from app.models.user import User


async def check_rate_limit(user: User) -> None:
    key = f"rate_limit:user:{user.id}"

    current_count = await redis_client.incr(key)

    if current_count == 1:
        await redis_client.expire(key, settings.RATE_LIMIT_WINDOW_SECONDS)

    if current_count > settings.RATE_LIMIT_MESSAGES:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded. Please try again later.",
        )