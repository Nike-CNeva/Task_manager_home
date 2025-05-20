from fastapi import APIRouter, Depends, status
from backend.app.core.dependencies import get_current_user
from fastapi.responses import JSONResponse
from datetime import datetime
from backend.app.models.user import User
from backend.app.schemas.user import UserRead



router = APIRouter()

@router.get("/", response_class=JSONResponse)
def home(user: User = Depends(get_current_user)):
    """
    Главная страница.
    """
    user_data = UserRead.model_validate(user).model_dump()
    current_datetime = datetime.now().isoformat()
    return JSONResponse({
        "user": user_data,
        "current_datetime": current_datetime,
    }, status_code=status.HTTP_200_OK)
