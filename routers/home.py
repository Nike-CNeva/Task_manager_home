from fastapi import APIRouter, Depends, status
from dependencies import get_current_user
from fastapi.responses import JSONResponse
from datetime import datetime
from schemas import UserRead


router = APIRouter()

@router.get("/", response_class=JSONResponse)
def home(user: UserRead = Depends(get_current_user)):
    """
    Главная страница.
    """
    current_datetime = datetime.now().isoformat()
    return JSONResponse({
        "user": user.dict(),
        "current_datetime": current_datetime,
    }, status_code=status.HTTP_200_OK)
