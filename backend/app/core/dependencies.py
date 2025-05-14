from fastapi import Depends, Request, HTTPException
from backend.app.database.database import get_db
from backend.app.schemas.user import UserRead
from services.user_service import get_user_by_id
from sqlalchemy.ext.asyncio import AsyncSession


async def get_current_user(request: Request, db: AsyncSession = Depends(get_db)) -> UserRead:
    user_id = getattr(request.state, 'user_id', None)
    if user_id is None:
        raise HTTPException(status_code=401, detail="Not authenticated")

    user = await get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return UserRead.model_validate(user)


