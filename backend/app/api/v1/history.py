from fastapi import APIRouter, Depends, Query

from app.core.auth import CurrentUser, get_current_user
from app.services.history_service import HistoryService

router = APIRouter(prefix="/history", tags=["history"])


@router.get("")
def get_history(
    limit: int = Query(20, ge=1, le=100),
    status: str | None = None,
    content_type: str | None = None,
    platform: str | None = None,
    current_user: CurrentUser = Depends(get_current_user),
) -> dict:
    kwargs = {
        "limit": limit,
        "status": status,
        "content_type": content_type,
        "platform": platform,
    }
    if not current_user.is_dev:
        kwargs["user_id"] = current_user.id
    return HistoryService().list_jobs(**kwargs)
