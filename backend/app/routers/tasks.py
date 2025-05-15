from fastapi import APIRouter, Depends, File, Form, HTTPException, Path, UploadFile, status
from fastapi.responses import JSONResponse
from typing import Any, Dict, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.core.dependencies import get_current_user, get_db
from backend.app.models.bid import Customer
from backend.app.models.enums import ManagerEnum, StatusEnum
from backend.app.models.user import User
from backend.app.schemas.bid import BidCreateResponse
from backend.app.schemas.customer import CustomerCreateRequest, CustomerRead
from backend.app.schemas.product import ProductResponse
from backend.app.schemas.task import TaskRead
from services import task_service, product_service, material_service
import json
import logging


router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/tasks", response_model=List[TaskRead])
async def get_tasks(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        tasks = await task_service.get_tasks_list(current_user, db)
        return tasks
    except Exception as e:
        logger.error(f"❌ Ошибка при получении задач: {e}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")
    

@router.get("/task/{task_id}", response_model=TaskRead)
async def get_task(task_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    task = await task_service.get_task_by_id(task_id, db)
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    return task


@router.post("/bids/create/", response_model=BidCreateResponse)
async def create_bid(
    bid_data: str = Form(...),
    files: List[UploadFile] = File(None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not authenticated")

    try:
        bid_data_dict = json.loads(bid_data)
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f"Ivalid bid data: {e}")

    try:
        bid_info = BidCreateResponse(**bid_data_dict)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f"Invalid bid data: {e}")

    try:
        result = await task_service.create_bid_with_tasks(bid_info, files, db)
        return result
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/customers/", response_model=List[CustomerRead])
async def get_customers(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Customer))
    customers = result.scalars().all()
    return customers

@router.get("/managers/", response_model=List[str])
async def get_managers():
    return [manager.value for manager in ManagerEnum]

@router.get("/statuses/", response_model=List[str])
async def get_status():
    return [status.value for status in StatusEnum]

@router.post("/customers/", response_model=dict)
async def add_customer(payload: CustomerCreateRequest, db: AsyncSession = Depends(get_db)):
    customer = Customer(name=payload.name)
    db.add(customer)
    await db.commit()
    await db.refresh(customer)
    return JSONResponse(content=customer, status_code=status.HTTP_201_CREATED)

@router.get("/products/", response_model=List[ProductResponse])
async def get_products(product_service: product_service.ProductService = Depends(product_service.get_product_service)):
    return await product_service.get_product_list()



@router.get("/products/{product_id}/fields", response_model=List[Dict[str, Any]])
async def get_product_fields(product_id: str, product_service: product_service.ProductService = Depends(product_service.get_product_service)):
    return product_service.get_product_fields(product_id)

@router.get("/material/forms/{product_id}", response_model=List[Dict[str, Any]])
async def get_material_forms(product_id: str, material_service: material_service.MaterialService = Depends(material_service.get_material_service)):
    return material_service.get_material_forms(product_id)


@router.get("/material/types/{product_id}/{form}", response_model=List[Dict[str, Any]])
async def get_material_types(product_id: str, form: str = Path(...), material_service: material_service.MaterialService = Depends(material_service.get_material_service)):
    return material_service.get_material_types(product_id, form)
