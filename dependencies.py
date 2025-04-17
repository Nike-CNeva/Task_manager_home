from typing import Optional
from fastapi import Depends, Request, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas import UserRead
from services.user_service import get_user_by_id



def get_current_user(request: Request, db: Session = Depends(get_db)) -> UserRead:
    user_id = getattr(request.state, 'user_id', None)
    if user_id is None:
        raise HTTPException(status_code=401, detail="Not authenticated")

    user = get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return UserRead.model_validate(user)
