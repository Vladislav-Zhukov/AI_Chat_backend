from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse

from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user
from app.auth.rate_limit import check_rate_limit
from app.chats.service import get_user_chat_by_id
from app.core.config import settings
from app.db.database import get_db
from app.models.user import User
from app.ai.factory import ai_client
from app.usage.service import create_usage_log
from app.messages.schemas import ChatResponse, MessageCreate, MessageRead
from app.messages.service import (
    create_assistant_message,
    create_user_message,
    get_chat_messages,
    get_recent_chat_messages,
)

router = APIRouter(prefix="/chats/{chat_id}/messages", tags=["Messages"])


@router.post("", response_model=ChatResponse, status_code=status.HTTP_201_CREATED)
async def create_message_endpoint(
    chat_id: int,
    data: MessageCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    chat = await get_user_chat_by_id(db, current_user.id, chat_id)

    if chat is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat not found",
        )

    await check_rate_limit(current_user)

    user_message = await create_user_message(db, chat.id, data)

    messages = await get_recent_chat_messages(
        db=db,
        chat_id=chat.id,
        limit=settings.AI_CONTEXT_MESSAGES_LIMIT,
    )

    ai_messages = [
        {
            "role": message.role,
            "content": message.content,
        }
        for message in messages
    ]

    ai_answer = await ai_client.generate_response(ai_messages)

    assistant_message = await create_assistant_message(
        db=db,
        chat_id=chat.id,
        content=ai_answer,
    )

    await create_usage_log(
        db=db,
        user_id=current_user.id,
        chat_id=chat.id,
        provider=settings.AI_PROVIDER,
        model=settings.OPENAI_MODEL if settings.AI_PROVIDER == "openai" else "mock",
    )

    return ChatResponse(
        user_message=user_message,
        assistant_message=assistant_message,
    )


@router.get("", response_model=list[MessageRead])
async def get_messages_endpoint(
    chat_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    chat = await get_user_chat_by_id(db, current_user.id, chat_id)

    if chat is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat not found",
        )

    return await get_chat_messages(db, chat.id)


@router.post("/stream")
async def stream_message_endpoint(
    chat_id: int,
    data: MessageCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    chat = await get_user_chat_by_id(db, current_user.id, chat_id)

    if chat is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat not found",
        )

    await check_rate_limit(current_user)

    user_message = await create_user_message(db, chat.id, data)

    messages = await get_recent_chat_messages(
        db=db,
        chat_id=chat.id,
        limit=settings.AI_CONTEXT_MESSAGES_LIMIT,
    )

    ai_messages = [
        {
            "role": message.role,
            "content": message.content,
        }
        for message in messages
    ]

    async def event_generator():
        full_answer = ""

        async for chunk in ai_client.stream_response(ai_messages):
            full_answer += chunk
            yield f"data: {chunk}\n\n"

        await create_assistant_message(
            db=db,
            chat_id=chat.id,
            content=full_answer,
        )

        await create_usage_log(
            db=db,
            user_id=current_user.id,
            chat_id=chat.id,
            provider=settings.AI_PROVIDER,
            model=settings.OPENAI_MODEL if settings.AI_PROVIDER == "openai" else "mock",
        )

        yield "data: [DONE]\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
    )