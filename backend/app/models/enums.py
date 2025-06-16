from enum import Enum

class ProductTypeEnum(str, Enum):
    PROFILE = "Профиля"
    KLAMER = "Клямера"
    BRACKET = "Кронштейны"
    EXTENSION_BRACKET = "Удлинители кронштейнов"
    CASSETTE = "Кассеты"
    FACING = "Фасонка"
    LINEAR_PANEL = "Линеарные панели"
    SHEET = "Листы"
    WALL_PANEL = "Стеновые панели(Продэкс)"

class UserTypeEnum(str, Enum):
    ADMIN = "Администратор"
    ENGINEER = "Инженер"
    OPERATOR = "Оператор"
    SUPERVISER = "Старший смены"
 
class ProfileTypeEnum(str, Enum):
    G40X40 = "Г-образный 40х40"
    G40X60 = "Г-образный 40х60"
    G50X50 = "Г-образный 50х50"
    P60 = "П-образный 60"
    P80 = "П-образный 80"
    P100 = "П-образный 100"
    Z20X20X40 = "З-образный 20х20х40"
    PGSH = "ПГШ"
    PVSH = "ПВШ"
    PNU = "ПНУ"

class WorkshopEnum(str, Enum):
    PROFILE = "Прокат профилей"
    KLAMER = "Прокат клямеров"
    BRACKET = "Прокат кронштейнов"
    EXTENSION_BRACKET = "Гибка удлинителей кронштейнов"
    ENGINEER = "Инженер"
    BENDING = "Гибка"
    CUTTING = "Резка"
    COORDINATE_PUNCHING = "Координатка"
    PAINTING = "Покраска"

class ManagerEnum(str, Enum):
    NOVIKOV = "Новиков"
    SEMICHEV = "Семичев С."
    PTICHKINA = "Птичкина"
    VIKULINA = "Викулина"
    GAVRILOVEC = "Гавриловец"
    SEMICHEV_YOUNGER = "Семичев Д."

class KlamerTypeEnum(str, Enum):
    IN_LINE = "Рядный"
    STARTING = "Стартовый"
    ANGULAR = "Угловой"

class CassetteTypeEnum(str, Enum):
    KZT_STD = "Закрытого типа(стандарт)"
    KOT_STD = "Открытого типа(стандарт)"
    KOTVO = "Открытого типа, отв. в вертикальных рустах"
    KZT = "Закрытого типа"
    KOT = "Открытого типа"
    OTHER = "Другое"

class MaterialTypeEnum(str, Enum):
    ALUMINIUM = "Алюминий"
    STEEL = "Сталь"
    STAINLESS_STEEL = "Нержавеющая сталь"
    ZINC = "Оцинковка"
    POLYMER = "Полимер"

class MaterialThicknessEnum(str, Enum):
    ZERO_FIVE = "0.5мм"
    ZERO_SEVEN = "0.7мм"
    ONE = "1.0мм"
    ONE_TWO = "1.2мм"
    ONE_FIVE = "1.5мм"
    TWO = "2.0мм"
    THREE = "3.0мм"

class UrgencyEnum(str, Enum):
    LOW = "Низкая"
    MEDIUM = "Нормальная"
    HIGH = "Высокая"

class StatusEnum(str, Enum):
    NEW = "Новая"
    IN_WORK = "В работе"
    COMPLETED = "Выполнена"
    CANCELED = "Отменена"
    ON_HOLD = "На удержании"

class FileType(str, Enum):
    PHOTO = "photo"     
    IMAGE = "image"      
    PDF = "pdf"
    NC = "nc"
    EXCEL = "excel"
    WORD = "word"
    DXF = "dxf"
    DWG = "dwg"
    SYSTEM = "system"