from hmac import new
import os
import shutil
from zipfile import ZipFile
from fastapi import APIRouter, Depends, File, Form, HTTPException, Path, UploadFile, status
from typing import List
from fastapi.responses import FileResponse
from sqlalchemy import func, select
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from websockets import Data
from backend.app.core.dependencies import get_current_user, get_db
from backend.app.models.bid import Bid, Customer
from backend.app.models.enums import CassetteTypeEnum, FileType, KlamerTypeEnum, ManagerEnum, MaterialThicknessEnum, MaterialTypeEnum, ProductTypeEnum, ProfileTypeEnum, StatusEnum, UrgencyEnum, WorkshopEnum
from backend.app.models.files import Files
from backend.app.models.material import Sheets
from backend.app.models.product import Product
from backend.app.models.task import Task, TaskProduct
from backend.app.models.user import User
from backend.app.models.workshop import WORKSHOP_ORDER, Workshop
from backend.app.schemas.bid import BidCreate
from backend.app.schemas.create_bid import ReferenceDataResponse
from backend.app.schemas.customer import CustomerRead
from backend.app.schemas.file import UploadedFileResponse
from backend.app.schemas.product_fields import get_product_fields
from backend.app.schemas.task import BidRead, FilesRead, MaterialUpdate, QuantityUpdateRequest, SheetsCreate
from backend.app.schemas.user import EmployeeOut
from backend.app.schemas.workshop import WorkshopRead
from backend.app.services import task_service
import json
import logging

from backend.app.services.file_service import get_files_for_bid, save_file


router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/tasks", response_model=List[BidRead])
async def get_tasks(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        tasks = await task_service.get_bids_with_tasks(current_user, db)
        return tasks
    except Exception as e:
        logger.error(f"❌ Ошибка при получении задач: {e}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")
    

@router.get("/task/{task_id}", response_model=BidRead)
async def get_task(task_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    task = await task_service.get_bid_by_task_id(task_id, db)
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    return task

@router.delete("/task/{task_id}/delete")
async def delete_task(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        # Поиск задачи с предзагрузкой заявки
        result = await db.execute(
            select(Task).options(joinedload(Task.bid)).where(Task.id == task_id)
        )
        task = result.scalar_one_or_none()

        if task is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Задача не найдена")

        bid_id = task.bid_id

        # Удаление задачи
        await db.delete(task)
        await db.commit()

        # Проверка: остались ли задачи у заявки
        result = await db.execute(
            select(func.count()).select_from(Task).where(Task.bid_id == bid_id)
        )
        remaining_tasks = result.scalar()

        if remaining_tasks == 0:
            # Получение заявки
            result = await db.execute(select(Bid).where(Bid.id == bid_id))
            bid = result.scalar_one_or_none()

            if bid:
                # Получение всех файлов, связанных с заявкой
                result = await db.execute(select(Files).where(Files.bid_id == bid_id))
                files = result.scalars().all()

                for file in files:
                    # Удаление файла с диска, если он существует
                    if file.file_path and os.path.exists(file.file_path):
                        try:
                            os.remove(file.file_path)
                        except Exception as e:
                            # Не критично, просто лог (если логируете)
                            print(f"Не удалось удалить файл {file.file_path}: {e}")

                    # Удаление записи файла из базы
                    await db.delete(file)

                # Удаление заявки
                await db.delete(bid)
                await db.commit()

                return {"message": "Задача и заявка удалены. Связанные файлы также удалены."}

        return {"message": "Задача успешно удалена"}

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
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
        fields: List[dict] = await get_product_fields(product["value"])
        products_data.append({
            "name": product["name"],
            "value": product["value"],
            "fields": fields
        })

    materials_data = [
        {"name": "material_type", "label": "Тип материала", "type": "select", "options": [{"value": type.value, "name": type.name} for type in MaterialTypeEnum]},
        {"name": "material_thickness", "label": "Толщина материала", "type": "select", "options": [{"value": thickness.value, "name": thickness.name} for thickness in MaterialThicknessEnum]},
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

@router.patch("/tasks/{task_id}/material")
async def update_material_data(
    task_id: int,
    data: MaterialUpdate,
    session: AsyncSession = Depends(get_db)
):
    result = await session.execute(
        select(Task).where(Task.id == task_id).options(selectinload(Task.material))
    )
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")

    if task.material:
        if data.weight is not None:
            if task.material.weight is None:
                task.material.weight = data.weight
            else:
                task.material.weight = task.material.weight + data.weight
        if data.waste is not None:
            task.material.waste = data.waste
        await session.commit()
        return {"success": True}
    else:
        raise HTTPException(status_code=404, detail="Материал не найден")

@router.post("/tasks/{bid_id}/files", response_model=List[FilesRead]) 
async def upload_file_to_task(
    bid_id: int,
    files: List[UploadFile] = File([]),
    db: AsyncSession = Depends(get_db)
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
    files_save = []
    for file in files:
        if '.' not in file.filename:
            raise HTTPException(status_code=400, detail="File must have an extension")
        ext = file.filename.rsplit('.', 1)[-1].lower()
        if ext not in ext_map:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Unsupported file extension: {ext}")
        file_save =  await save_file(bid_id, file, db)
        files_save.append(file_save)
    return files_save

@router.patch("/tasks/{task_id}/status")
async def update_workshop_status(
    task_id: int,
    new_status: StatusEnum,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Task).options(selectinload(Task.workshops)).where(Task.id == task_id)
    )
    task = result.scalars().first()

    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")

    task_workshops = sorted(task.workshops, key=lambda w: WORKSHOP_ORDER.index(w.workshop.name))

    # Получаем Enum-значения цехов пользователя
    user_workshop_names = {w.name for w in current_user.workshops}

    # Отфильтровываем TaskWorkshop, к которым у пользователя есть доступ
    user_workshops = [w for w in task_workshops if w.workshop.name in user_workshop_names]

    if not user_workshops:
        raise HTTPException(status_code=403, detail="Нет доступа к цехам задачи")

    # Находим первый доступный для пользователя цех, который не "Выполнена"
    target_workshop = next(
        (
            w for w in task_workshops
            if w.workshop.name in user_workshop_names and w.status != "Выполнена"
        ),
        None
    )

    if not target_workshop:
        raise HTTPException(status_code=400, detail="Нет подходящего цеха для обновления")

    target_index = task_workshops.index(target_workshop)

    for prev_workshop in task_workshops[:target_index]:
        if prev_workshop.status != "Выполнена":
            raise HTTPException(status_code=400, detail="Предыдущие цеха не завершены")

    target_workshop.status = new_status

    if target_index == 0 and new_status == "В работе":
        for w in task_workshops[1:]:
            w.status = "На удержании"

    statuses = [w.status for w in task_workshops]
    if all(status == "Выполнена" for status in statuses):
        task.status = "Выполнена"
    elif any(status == "В работе" for status in statuses):
        task.status = "В работе"

    await db.commit()

    return {
        "task_status": task.status,
        "workshops": [
            {"id": w.id, "workshop_name": w.workshop.name, "status": w.status}
            for w in task_workshops
        ]
    }

@router.post("/tasks/{task_id}/add_quantity")
async def update_task_done_quantity(
    task_id: int,
    quantities: QuantityUpdateRequest,
    session: AsyncSession = Depends(get_db)
):
    updated_task_products = []

    for item in quantities.quantities:
        # Найти TaskProduct по task_id и product_id
        stmt = select(TaskProduct).where(
            TaskProduct.task_id == task_id,
            TaskProduct.product_id == item.product_id
        )
        result = await session.execute(stmt)
        task_product = result.scalar_one_or_none()

        if not task_product:
            raise HTTPException(
                status_code=404,
                detail=f"TaskProduct с task_id={task_id} и product_id={item.product_id} не найден"
            )

        new_done_quantity = task_product.done_quantity + item.quantity
        if new_done_quantity > task_product.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Превышено максимальное количество для product_id={item.product_id}"
            )

        task_product.done_quantity = new_done_quantity
        updated_task_products.append(task_product)

    # Получаем задачу со связанными продуктами и цехами
    stmt_task = select(Task).where(Task.id == task_id).options(
        selectinload(Task.task_products),
        selectinload(Task.workshops),
    )
    result = await session.execute(stmt_task)
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")

    progress = task.progress_percent

    # Обновляем прогресс по цехам
    for workshop in task.workshops:
        workshop.progress_percent = progress

    await session.commit()

    # Ответ
    response = [
        {
            "product_id": tp.product_id,
            "done_quantity": tp.done_quantity
        } for tp in updated_task_products
    ]

    return {
        "updated_products": response,
        "updated_progress_percent": progress
    }

@router.post("/tasks/{task_id}/sheets")
async def upload_sheets(
    data: SheetsCreate,
    db: AsyncSession = Depends(get_db)
):
    new_sheet = Sheets(
        width=data.width,
        length=data.length,
        quantity=data.quantity,
        task_id=data.task_id
    )
    db.add(new_sheet)
    await db.commit()
    return  {
                "id": new_sheet.id,
                "count": new_sheet.quantity,
                "width": new_sheet.width,
                "length": new_sheet.length
            }

@router.delete("/tasks/{task_id}/sheets/{sheet_id}")
async def delete_sheet(
    task_id: int,
    sheet_id: int,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Sheets).where(Sheets.id == sheet_id)
    )
    sheet = result.scalar_one_or_none()
    if not sheet:
        raise HTTPException(status_code=404, detail="Лист не найден")
    if sheet.task_id != task_id:
        raise HTTPException(status_code=400, detail="Лист не принадлежит задаче")
    await db.delete(sheet)
    await db.commit()
    return {"success": True}


