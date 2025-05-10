from fastapi import APIRouter, Depends, File, Form, HTTPException, Path, UploadFile, status
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from typing import List
from dependencies import get_current_user, get_db
from models import Customer, ManagerEnum, StatusEnum, User
from schemas import BidCreateRequest, CustomerCreateRequest, CustomerRead, ProductResponse, TaskRead
from services import task_service, product_service, material_service
import json


router = APIRouter()


@router.get("/tasks", response_model=List[TaskRead])
async def get_tasks(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        tasks = task_service.get_tasks_list(current_user, db)
        return tasks
    except Exception as e:
        print("❌ Ошибка:", e)
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/task/{task_id}", response_model=dict)
def get_task(task_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    task = task_service.get_task_by_id(task_id, db)
    return JSONResponse(content=task)


@router.post("/bids/create/", response_model=dict)
def create_bid(
    bid_data: str = Form(...),
    files: List[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not authenticated")

    try:
        bid_data_dict = json.loads(bid_data)
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f"Invalid bid data: {e}")

    try:
        bid_info = BidCreateRequest(**bid_data_dict)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f"Invalid bid data: {e}")

    try:
        result = task_service.create_bid_with_tasks(bid_info, files, db, current_user)
        return JSONResponse(content=result, status_code=status.HTTP_201_CREATED)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/customers/", response_model=List[CustomerRead])
def get_customers(db: Session = Depends(get_db)):
    customers = db.query(Customer).all()
    return customers

@router.get("/managers/", response_model=List[str])
def get_managers():
    return [manager.value for manager in ManagerEnum]

@router.get("/statuses/", response_model=List[str])
def get_status():
    return [status.value for status in StatusEnum]

@router.post("/customers/", response_model=dict)
def add_customer(payload: CustomerCreateRequest, db: Session = Depends(get_db)):
    customer = Customer(name=payload.name)
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return JSONResponse(content=customer, status_code=status.HTTP_201_CREATED)

@router.get("/products/", response_model=List[ProductResponse])
def get_products(product_service: product_service.ProductService = Depends(product_service.get_product_service)):
    return product_service.get_product_list()



@router.get("/products/{product_id}/fields", response_model=List[dict])
def get_product_fields(product_id: str, db: Session = Depends(get_db), product_service: product_service.ProductService = Depends(product_service.get_product_service)):
    return product_service.get_product_fields(product_id)

@router.get("/material/forms/{product_id}", response_model=List[dict])
def get_material_forms(product_id: str, material_service: material_service.MaterialService = Depends(material_service.get_material_service)):
    return material_service.get_material_forms(product_id)


@router.get("/material/types/{product_id}/{form}", response_model=List[dict])
def get_material_types(product_id: str, form: str = Path(...), material_service: material_service.MaterialService = Depends(material_service.get_material_service)):
    return material_service.get_material_types(product_id, form)
