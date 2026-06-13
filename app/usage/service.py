from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.usage import UsageLog


async def create_usage_log(
    db: AsyncSession,
    user_id: int,
    chat_id: int,
    provider: str,
    model: str,
    prompt_tokens: int = 0,
    completion_tokens: int = 0,
    total_tokens: int = 0,
) -> UsageLog:
    usage_log = UsageLog(
        user_id=user_id,
        chat_id=chat_id,
        provider=provider,
        model=model,
        prompt_tokens=prompt_tokens,
        completion_tokens=completion_tokens,
        total_tokens=total_tokens,
    )

    db.add(usage_log)
    await db.commit()
    await db.refresh(usage_log)

    return usage_log


async def get_user_usage_stats(db: AsyncSession, user_id: int) -> dict:
    result = await db.execute(
        select(
            func.count(UsageLog.id),
            func.coalesce(func.sum(UsageLog.prompt_tokens), 0),
            func.coalesce(func.sum(UsageLog.completion_tokens), 0),
            func.coalesce(func.sum(UsageLog.total_tokens), 0),
        ).where(UsageLog.user_id == user_id)
    )

    count, prompt_tokens, completion_tokens, total_tokens = result.one()

    return {
        "requests_count": count,
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "total_tokens": total_tokens,
    }