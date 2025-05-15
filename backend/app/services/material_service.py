from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.core.dependencies import get_db
from backend.app.database.database_service import AsyncDatabaseService
from typing import Generator, List, Dict, Any
from fastapi import Depends

from backend.app.models.enums import MaterialFormEnum, MaterialTypeEnum, ProductTypeEnum

class MaterialService:
    def __init__(self, db: AsyncSession):
        self.db_service = AsyncDatabaseService(db)

    async def get_material_forms(self, product_id: str) -> List[Dict[str, Any]]:
        """
        Получает список форм материалов для конкретного продукта.
        """
        if product_id == ProductTypeEnum.SHEET:
            return [{"id": form.value, "name": form.value} for form in MaterialFormEnum]
        else:
            return [{"id": MaterialFormEnum.SHEET.value, "name": MaterialFormEnum.SHEET.value}]

    async def get_material_types(self, product_id: str, form: str) -> List[Dict[str, Any]]:
        """
        Получает список типов материалов для конкретного продукта и формы.
        """
        if product_id == ProductTypeEnum.SHEET and form == MaterialFormEnum.SHEET.value:
            return [
                {"id": type.value, "name": type.value} for type in MaterialTypeEnum
            ]
        elif product_id == ProductTypeEnum.PROFILE and form == MaterialFormEnum.SHEET.value:
            return [
                {"id": type.value, "name": type.value} for type in MaterialTypeEnum
            ]
        elif product_id == ProductTypeEnum.KLAMER and form == MaterialFormEnum.SHEET.value:
            return [
                {"id": type.value, "name": type.value} for type in MaterialTypeEnum
            ]
        elif product_id == ProductTypeEnum.BRACKET and form == MaterialFormEnum.SHEET.value:
            return [
                {"id": type.value, "name": type.value} for type in MaterialTypeEnum
            ]
        elif product_id == ProductTypeEnum.EXTENSION_BRACKET and form == MaterialFormEnum.SHEET.value:
            return [
                {"id": type.value, "name": type.value} for type in MaterialTypeEnum
            ]
        elif product_id == ProductTypeEnum.CASSETTE and form == MaterialFormEnum.SHEET.value:
            return [
                {"id": type.value, "name": type.value} for type in MaterialTypeEnum
            ]
        elif product_id == ProductTypeEnum.LINEAR_PANEL and form == MaterialFormEnum.SHEET.value:
            return [
                {"id": type.value, "name": type.value} for type in MaterialTypeEnum
            ]
        else:
            return []
        
def get_material_service(db: AsyncSession = Depends(get_db)) -> Generator[MaterialService, None, None]:
    yield MaterialService(db)