from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.core.dependencies import get_current_user, get_db
from backend.app.models.bid import Customer
from backend.app.models.enums import CassetteTypeEnum, FileType, KlamerTypeEnum, ManagerEnum, MaterialFormEnum, MaterialThicknessEnum, MaterialTypeEnum, ProductTypeEnum, ProfileTypeEnum, StatusEnum, UrgencyEnum, WorkshopEnum
from backend.app.models.product import Product
from backend.app.models.user import User
from backend.app.models.workshop import Workshop
from backend.app.schemas.bid import BidCreate
from backend.app.schemas.create_bid import ReferenceDataResponse
from backend.app.schemas.customer import CustomerRead
from backend.app.schemas.task import TaskRead
from backend.app.schemas.user import EmployeeOut
from backend.app.schemas.workshop import WorkshopRead
from backend.app.services import task_service
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


@router.post("/bids/create/")
async def create_bid(
    bid_data: str = Form(...),
    files: List[UploadFile] = File([]),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Валидация файлов по расширениям
    ext_map = {
        "jpg": FileType.PHOTO,
        "jpeg": FileType.PHOTO,
        "png": FileType.IMAGE,
        "pdf": FileType.PDF,
        "nc": FileType.NC,
        "xls": FileType.EXCEL,
        "xlsx": FileType.EXCEL,
        "doc": FileType.WORD,
        "docx": FileType.WORD,
        "dxf": FileType.DXF,
        "dwg": FileType.DWG,
    }
    for file in files:
        if '.' not in file.filename:
            raise HTTPException(status_code=400, detail="File must have an extension")
        ext = file.filename.rsplit('.', 1)[-1].lower()
        if ext not in ext_map:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Unsupported file extension: {ext}")

    try:
        bid_data_dict = json.loads(bid_data)
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f"Invalid bid data: {e}")

    # Обработка customer_id == "new"
    if bid_data_dict.get("customer") == "new":
        customer_name = bid_data_dict.get("new_customer")
        if not customer_name or not customer_name.strip():
            raise HTTPException(status_code=422, detail="Customer name is required")
        new_customer = await task_service.create_new_customer_async(db, customer_name)  # реализуй сам
        bid_data_dict["customer"] = new_customer.id  # заменяем строку "new" на реальный id
        bid_data_dict["new_customer"] = None

    try:
        bid_info = BidCreate(**bid_data_dict)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f"Invalid bid data: {e}")

    try:
        result = await task_service.create_bid_with_tasks(current_user, bid_info, files, db)
        return result
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/reference-data/", response_model=ReferenceDataResponse)
async def get_reference_data(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Customer))
    customers: List[CustomerRead] = result.scalars().all()

    result = await db.execute(select(User))
    employees: List[EmployeeOut] = result.scalars().all()

    products = [{"name": product.name, "value": product.value} for product in ProductTypeEnum]
    products_data = []

    for product in products:
        if product["value"] == ProductTypeEnum.PROFILE:
            fields = [
                {"name": "profile_type", "label": "Тип профиля", "type": "select", "options": [{"value": pt.value, "name": pt.name} for pt in ProfileTypeEnum]},
                {"name": "length", "label": "Введите длину профиля", "type": "number"},
                {"name": "quantity", "label": "Введите количество профилей", "type": "number"}
            ]
        elif product["value"] == ProductTypeEnum.KLAMER:
            fields = [
                {"name": "klamer_type_id", "label": "Тип клямера", "type": "select", "options": [{"value": kt.value, "name": kt.name} for kt in KlamerTypeEnum]},
                {"name": "quantity", "label": "Введите количество клямеров", "type": "number"}
            ]
        elif product["value"] == ProductTypeEnum.BRACKET:
            fields = [
                {"name": "width", "label": "Ширина", "type": "number"},
                {"name": "length", "label": "Длина", "type": "text"},
                {"name": "quantity", "label": "Количество кронштейнов", "type": "number"}
            ]
        elif product["value"] == ProductTypeEnum.EXTENSION_BRACKET:
            fields = [
                {"name": "width", "label": "Ширина", "type": "number"},
                {"name": "length", "label": "Длина", "type": "text"},
                {"name": "has_heel", "label": "Наличие пятки", "type": "checkbox"},
                {"name": "quantity", "label": "Количество удлинителей", "type": "number"}
            ]
        elif product["value"] == ProductTypeEnum.CASSETTE:
            fields = [
                {"name": "cassette_type", "label": "Тип кассеты", "type": "select", "options": [{"value": ct.value, "name": ct.name} for ct in CassetteTypeEnum]},
                {"name": "description", "label": "Введите описание", "type": "text"},
                {"name": "quantity", "label": "Введите количество кассет", "type": "number"}
            ]
        elif product["value"] == ProductTypeEnum.LINEAR_PANEL:
            fields = [
                {"name": "panel_width", "label": "Поле", "type": "number"},
                {"name": "groove", "label": "Руст", "type": "number"},
                {"name": "length", "label": "Длина", "type": "number"},
                {"name": "has_endcap", "label": "Наличие торцевания", "type": "checkbox"},
                {"name": "quantity", "label": "Количество панелей", "type": "number"}
            ]
        elif product["value"] == ProductTypeEnum.SHEET:
            fields = []
        else:
            fields = [{"name": "quantity", "label": "Количество", "type": "number"}]

        products_data.append({
            "name": product["name"],
            "value": product["value"],
            "fields": fields
        })

    materials_data = [
        {"name": "material_form", "label": "Форма материала", "type": "select", "options": [{"value": form.value, "name": form.name} for form in MaterialFormEnum]},
        {"name": "material_type", "label": "Тип материала", "type": "select", "options": [{"value": type.value, "name": type.name} for type in MaterialTypeEnum]},
        {"name": "material_thickness", "label": "Толщина материала", "type": "select", "options": [{"value": thickness.value, "name": thickness.name} for thickness in MaterialThicknessEnum]},
        {"name": "painting", "label": "Красится", "type": "checkbox"},
        {"name": "color", "label": "Цвет", "type": "text"}
    ]

    return {
        "customers": [{"id": customer.id, "name": customer.name} for customer in customers],
        "managers": [{"name": manager.name, "value": manager.value} for manager in ManagerEnum],
        "urgency": [{"name": urgency.name, "value": urgency.value} for urgency in UrgencyEnum],
        "products": products_data,
        "materials": materials_data,
        "workshops": [{"name": workshop.name, "value": workshop.value} for workshop in WorkshopEnum],
        "employees": [{"id": employee.id, "name": employee.name, "firstname": employee.firstname} for employee in employees]
    }