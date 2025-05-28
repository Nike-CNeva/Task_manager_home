

from backend.app.models.enums import ProductTypeEnum


product_fields_by_type = {
    ProductTypeEnum.PROFILE: [
        {"name": "profile_type", "label": "Тип профиля", "type": "select"},
        {"name": "length", "label": "Длина профиля", "type": "number"},
    ],
    ProductTypeEnum.KLAMER: [
        {"name": "klamer_type", "label": "Тип клямера", "type": "select"},
    ],
    ProductTypeEnum.BRACKET: [
        {"name": "width", "label": "Ширина", "type": "number"},
        {"name": "length", "label": "Длина", "type": "text"},
    ],
    ProductTypeEnum.EXTENSION_BRACKET: [
        {"name": "width", "label": "Ширина", "type": "number"},
        {"name": "length", "label": "Длина", "type": "text"},
        {"name": "has_heel", "label": "Наличие пятки", "type": "checkbox"},
    ],
    ProductTypeEnum.CASSETTE: [
        {"name": "cassette_type", "label": "Тип кассеты", "type": "select"},
        {"name": "description", "label": "Описание", "type": "text"},
    ],
    ProductTypeEnum.LINEAR_PANEL: [
        {"name": "panel_width", "label": "Поле", "type": "number"},
        {"name": "groove", "label": "Руст", "type": "number"},
        {"name": "length", "label": "Длина", "type": "number"},
        {"name": "has_endcap", "label": "Наличие торцевания", "type": "checkbox"},
    ],
    ProductTypeEnum.SHEET: [],
}

async def get_product_fields(product_type: str):
    enum_type = ProductTypeEnum(product_type)
    return product_fields_by_type[enum_type]