from sqlalchemy.orm import Session
from dependencies import get_db
from models import Product, ProductTypeEnum, ProfileTypeEnum
from database_service import DatabaseService
from typing import List, Dict, Any
from fastapi import Depends, HTTPException

from schemas import ProductResponse

class ProductService:
    def __init__(self, db: Session):
        self.db_service = DatabaseService(db)

    def get_product_list(self) -> List[ProductResponse]:
        """
        Получает список всех продуктов.
        """
        products = self.db_service.get_all(Product)
        return [ProductResponse(id=p.id, type=p.type) for p in products]

    def get_product_fields(self, product_id: str) -> List[Dict[str, Any]]:
        """
        Получает список полей для конкретного продукта.
        """
        product = self.db_service.get_by_id(Product, int(product_id))
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        if product.type == ProductTypeEnum.PROFILE:
            return [{"id": pt.id, "name": pt.name} for pt in ProfileTypeEnum]
        elif product.type == ProductTypeEnum.KLAMER:
            return [{"id": 1, "name": "Рядный"}, {"id": 2, "name": "Стартовый"}, {"id": 3, "name": "Угловой"}]
        elif product.type == ProductTypeEnum.BRACKET:
            return [{"id": 1, "name": "Ширина"}, {"id": 2, "name": "Длина"}, {"id": 3, "name": "Толщина"}]
        elif product.type == ProductTypeEnum.EXTENSION_BRACKET:
            return [{"id": 1, "name": "Ширина"}, {"id": 2, "name": "Длина"}, {"id": 3, "name": "Наличие пятки"}]
        elif product.type == ProductTypeEnum.CASSETTE:
            return [{"id": 1, "name": "Закрытого типа(стандарт)"}, {"id": 2, "name": "Открытого типа(стандарт)"}, {"id": 3, "name": "Открытого типа, отв. в вертикальных рустах"}, {"id": 4, "name": "Закрытого типа"}, {"id": 5, "name": "Открытого типа"}, {"id": 6, "name": "Другое"}]
        elif product.type == ProductTypeEnum.LINEAR_PANEL:
            return [{"id": 1, "name": "Поле"}, {"id": 2, "name": "Руст"}, {"id": 3, "name": "Длина"}, {"id": 4, "name": "Наличие торцевания"}]
        elif product.type == ProductTypeEnum.SHEET:
            return [{"id": 1, "name": "Ширина"}, {"id": 2, "name": "Длина"}, {"id": 3, "name": "Количество"}]
        else:
            return []

def get_product_service(db: Session = Depends(get_db)) -> ProductService:
    return ProductService(db)
