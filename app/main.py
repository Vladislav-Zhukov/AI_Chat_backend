from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db.database import get_db

app = FastAPI(title = settings.APP_NAME)

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