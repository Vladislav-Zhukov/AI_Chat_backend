from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.functions import current_user

from app.auth.dependencies import get_current_user
from app.chats.schemas import ChatCreate, ChatRead, ChatUpdate
from app.chats.service import (
    create_chat,
    delete_chat,
    get_user_chat_by_id,
    get_user_chats,
    update_chat,
)
from app.db.database import get_db
from app.models.user import User

router = APIRouter(prefix="/chats", tags=["Chats"])


@router.post("", response_model=ChatRead, status_code=status.HTTP_201_CREATED)
async def create_chat_endpoint(
    data: ChatCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await create_chat(db, current_user.id, data)


@router.get("", response_model=list[ChatRead])
async def get_chat_endpoint(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await get_user_chats(db, current_user.id)


@router.get("/{chat_id}", response_model=ChatRead)
async def get_chat_endpoint(
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

    return chat


@router.patch("/{chat_id}", response_model=ChatRead)
async def update_chat_endpoint(
    chat_id: int,
    data: ChatUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    chat = await get_user_chat_by_id(db, current_user.id, chat_id)

    if chat is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat not found",
        )

    return await update_chat(db, chat, data)


@router.delete("/{chat_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_chat_endpoint(
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

    await delete_chat(db, chat)