from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.router import router as auth_router
from app.users.router import router as users_router
from app.chats.router import router as chats_router
from app.messages.router import router as messages_router

from app.core.config import settings
from app.db.database import get_db


app = FastAPI(title = settings.APP_NAME)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(chats_router)
app.include_router(messages_router)


@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.get("/db-check")
async def db_check(db: AsyncSession = Depends(get_db)):
    result = await db.executor(text("SELECT 1"))
    return {
        "status": "db ok",
        "result": result.scalar(),
    }