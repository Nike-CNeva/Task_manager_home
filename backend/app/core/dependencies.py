from fastapi import Depends, Request, HTTPException
from backend.app.database.database import get_db
from backend.app.models.user import User

from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.services.user_service import get_user_by_id


async def get_current_user(request: Request, db: AsyncSession = Depends(get_db)) -> User:
    user_id = getattr(request.state, 'user_id', None)
    if user_id is None:
        raise HTTPException(status_code=401, detail="Not authenticated")

    user = await get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user


