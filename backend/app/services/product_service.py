from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.core.dependencies import get_db
from backend.app.database.database_service import AsyncDatabaseService
from typing import List, Dict, Any
from fastapi import Depends, HTTPException

from backend.app.models.enums import ProductTypeEnum, ProfileTypeEnum
from backend.app.models.product import Product
from backend.app.schemas.product import ProductResponse



class ProductService:
    def __init__(self, db: AsyncSession):
        self.db_service = AsyncDatabaseService(db)

    async def get_product_list(self) -> List[ProductResponse]:
        """
        Получает список всех продуктов.
        """
        products = await self.db_service.get_all(Product)
        return [ProductResponse(id=p.id, type=p.type) for p in products]

    async def get_product_fields(self, product_id: str) -> List[Dict[str, Any]]:
        """
        Получает список полей для конкретного продукта, в формате, понятном фронтенду.
        """
        product = await self.db_service.get_by_id(Product, int(product_id))
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        if product.type == ProductTypeEnum.PROFILE:
            return [{
                "name": "profile_type",
                "label": "Тип профиля",
                "type": "select",
                "options": [{"value": pt.value, "label": pt.name} for pt in ProfileTypeEnum]
            },{
                "name": "Length",
                "label": "Введите длину профиля",
                "type": "number"
            },{
                "name": "Quantity",
                "label": "Введите количество профилей",
                "type": "number"
            }]

        elif product.type == ProductTypeEnum.KLAMER:
            return [{
                "name": "klamer_type_id",
                "label": "Тип клямера",
                "type": "select",
                "options": [
                    {"value": 1, "label": "Рядный"},
                    {"value": 2, "label": "Стартовый"},
                    {"value": 3, "label": "Угловой"},
                ]
            },{
                "name": "Quantity",
                "label": "Введите количество клямеров",
                "type": "number"
            }]

        elif product.type == ProductTypeEnum.BRACKET:
            return [
                {"name": "width", "label": "Ширина", "type": "number"},
                {"name": "length", "label": "Длина", "type": "number"},
                {"name": "thickness", "label": "Толщина", "type": "number"},
                {"name": "Quantity", "label": "Количество кронштейнов", "type": "number"}
            ]

        elif product.type == ProductTypeEnum.EXTENSION_BRACKET:
            return [
                {"name": "width", "label": "Ширина", "type": "number"},
                {"name": "length", "label": "Длина", "type": "number"},
                {"name": "has_heel", "label": "Наличие пятки", "type": "checkbox"},
            ]

        elif product.type == ProductTypeEnum.CASSETTE:
            return [{
                "name": "cassette_type_id",
                "label": "Тип кассеты",
                "type": "select",
                "options": [
                    {"value": "1", "label": "Закрытого типа(стандарт)"},
                    {"value": "2", "label": "Открытого типа(стандарт)"},
                    {"value": "3", "label": "Открытого типа, отв. в вертикальных рустах"},
                    {"value": "4", "label": "Закрытого типа"},
                    {"value": "5", "label": "Открытого типа"},
                    {"value": "OTHER", "label": "Другое"},
                ]
            }]

        elif product.type == ProductTypeEnum.LINEAR_PANEL:
            return [
                {"name": "panel_width", "label": "Поле", "type": "number"},
                {"name": "groove", "label": "Руст", "type": "number"},
                {"name": "length", "label": "Длина", "type": "number"},
                {"name": "has_endcap", "label": "Наличие торцевания", "type": "checkbox"},
            ]

        elif product.type == ProductTypeEnum.SHEET:
            return [
                {"name": "sheet_width", "label": "Ширина", "type": "number"},
                {"name": "sheet_length", "label": "Длина", "type": "number"},
                {"name": "quantity", "label": "Количество", "type": "number"},
            ]

        return []


def get_product_service(db: AsyncSession = Depends(get_db)) -> ProductService:
    return ProductService(db)
