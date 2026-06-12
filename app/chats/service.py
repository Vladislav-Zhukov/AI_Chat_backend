from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.chats.schemas import ChatCreate, ChatUpdate
from app.models.chat import Chat


async def create_chat(db: AsyncSession, user_id: int, data: ChatCreate) -> Chat:
    chat = Chat(
        user_id=user_id,
        title=data.title,
    )

    db.add(chat)
    await db.commit()
    await db.refresh(chat)

    return chat


async def get_user_chats(db: AsyncSession, user_id: int) -> list[Chat]:
    result = await db.execute(
        select(Chat)
        .where(Chat.user_id == user_id)
        .order_by(Chat.created_at.desc())
    )
    return list(result.scalars().all())


async def get_user_chat_by_id(
    db: AsyncSession,
    user_id: int,
    chat_id: int
) -> Chat | None:
    result = await db.execute(
        select(Chat).where(
            Chat.id == chat_id,
            Chat.user_id == user_id,
        )
    )
    return result.scalar_one_or_none()


async def update_chat(
    db: AsyncSession,
    chat: Chat,
    data: ChatUpdate
) -> Chat:
    chat.title = data.title

    await db.commit()
    await db.refresh(chat)

    return chat


async def delete_chat(db: AsyncSession, chat: Chat) -> None:
    await db.delete(chat)
    await db.commit()