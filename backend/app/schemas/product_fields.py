

from backend.app.models.enums import CassetteTypeEnum, KlamerTypeEnum, ProductTypeEnum, ProfileTypeEnum


product_fields_by_type = {
    ProductTypeEnum.PROFILE: [
        {"name": "profile_type", "label": "Тип профиля", "type": "select", "options": [{"value": pt.value, "name": pt.name} for pt in ProfileTypeEnum]},
        {"name": "length", "label": "Длина профиля", "type": "number"},
    ],
    ProductTypeEnum.KLAMER: [
        {"name": "klamer_type", "label": "Тип клямера", "type": "select", "options": [{"value": kt.value, "name": kt.name} for kt in KlamerTypeEnum]},
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
        {"name": "cassette_type", "label": "Тип кассеты", "type": "select", "options": [{"value": ct.value, "name": ct.name} for ct in CassetteTypeEnum]},
    ],
    ProductTypeEnum.LINEAR_PANEL: [
        {"name": "field", "label": "Поле", "type": "number"},
        {"name": "rust", "label": "Руст", "type": "number"},
        {"name": "length", "label": "Длина", "type": "number"},
        {"name": "butt_end", "label": "Наличие торцевания", "type": "checkbox"},
    ],
    ProductTypeEnum.SHEET: [],
}

fields = [{"name": "description", "label": "Описание", "type": "text"},
          {"name": "quantity", "label": "Количество", "type": "number"},
          {"name": "color", "label": "Цвет", "type": "text"},
          {"name": "painting", "label": "Красится?", "type": "checkbox"}]

async def get_product_fields(product_type: str):
    try:
        enum_type = ProductTypeEnum(product_type)
        # создаём новый список как конкатенацию
        field = product_fields_by_type.get(enum_type, []) + fields
        return field
    except ValueError:
        return list(fields)