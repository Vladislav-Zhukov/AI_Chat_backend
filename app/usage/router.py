from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.usage.schemas import UsageStatsRead
from app.usage.service import get_user_usage_stats

router = APIRouter(prefix="/users/me/usage", tags=["Usage"])


@router.get("", response_model=UsageStatsRead)
async def get_my_usage(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await get_user_usage_stats(db, current_user.id)