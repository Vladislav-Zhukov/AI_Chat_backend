from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user
from app.chats.service import get_user_chat_by_id
from app.db.database import get_db
from app.messages.schemas import MessageCreate, MessageRead
from app.messages.service import create_user_message, get_chat_messages
from app.models.user import User

router = APIRouter(prefix="/chats/{chat_id}/messages", tags=["Messages"])


@router.post("", response_model=MessageRead, status_code=status.HTTP_201_CREATED)
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

    return await create_user_message(db, chat.id, data)


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