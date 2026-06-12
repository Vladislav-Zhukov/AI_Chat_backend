from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.messages.schemas import MessageCreate
from app.models.message import Message


async def create_user_message(
    db: AsyncSession,
    chat_id: int,
    data: MessageCreate,
) -> Message:
    message = Message(
        chat_id=chat_id,
        role="user",
        content=data.content,
    )

    db.add(message)
    await db.commit()
    await db.refresh(message)

    return message


async def get_chat_messages(
    db: AsyncSession,
    chat_id: int,
) -> list[Message]:
    result = await db.execute(
        select(Message)
        .where(Message.chat_id == chat_id)
        .order_by(Message.created_at.asc())
    )

    return list(result.scalars().all())


async def create_assistant_message(
        db: AsyncSession,
        chat_id: int,
        content: str,
) -> Message:
    message = Message(
        chat_id = chat_id,
        role="assistant",
        content=content,
    )

    db.add(message)
    await db.commit()
    await db.refresh(message)

    return message


async def get_recent_chat_messages(
    db: AsyncSession,
    chat_id: int,
    limit: int,
) -> list[Message]:
    result = await db.execute(
        select(Message)
        .where(Message.chat_id == chat_id)
        .order_by(Message.created_at.desc())
        .limit(limit)
    )

    messages = list(result.scalars().all())

    return list(reversed(messages))