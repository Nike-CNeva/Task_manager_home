import os
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from backend.app.database.database import AsyncSessionLocal
from backend.app.database.database_service import AsyncDatabaseService
from backend.app.models.enums import ProductTypeEnum, WorkshopEnum
from backend.app.models.product import Product
from backend.app.models.workshop import Workshop
from backend.app.routers import users, tasks, files, comments, auth, home
from backend.app.core.settings import settings
from backend.app.middlewares.auth_middleware import AuthMiddleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager


#@asynccontextmanager
#async def lifespan(app: FastAPI):
#    async with AsyncSessionLocal() as session:
#        db_service = AsyncDatabaseService(session)
#        await db_service.ensure_enum_seeded(Workshop, WorkshopEnum)
#        await db_service.ensure_enum_seeded(Product, ProductTypeEnum, enum_field="type")
#    yield
#    await session.close()

app = FastAPI(
    title="Система управления задачами для производства",
    description="API для управления задачами, пользователями, файлами и комментариями в производственной системе.",
    version="1.0",
    debug=settings.DEBUG,
#    lifespan=lifespan
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Подключаем Middleware
app.add_middleware(AuthMiddleware)


# Подключение роутеров
app.include_router(home.router, prefix="/api", tags=["Главная"])
app.include_router(users.router, prefix="/api", tags=["Пользователи"])
app.include_router(tasks.router, prefix="/api", tags=["Задачи"])
app.include_router(files.router, prefix="/api", tags=["Файлы"])
app.include_router(comments.router, prefix="/api", tags=["Комментарии"])
app.include_router(auth.router, prefix="/api", tags=["Авторизация"])

# Путь к фронтенду
frontend_dir = os.path.join(os.path.dirname(__file__), "static")
assets_dir = os.path.join(frontend_dir, "assets")

app.mount("/static", StaticFiles(directory=frontend_dir), name="static")
app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")
# Отдаём index.html по умолчанию
@app.get("/")
def serve_frontend():
    return FileResponse(os.path.join(frontend_dir, "index.html"))


@app.get("/{full_path:path}")
async def serve_spa_fallback(request: Request, full_path: str):
    # Если путь начинается с /api — 404 или 401, НЕ отдаём index.html
    if full_path.startswith("api"):
        return JSONResponse(status_code=404, content={"detail": "Not Found"})

    return FileResponse(os.path.join(frontend_dir, "index.html"))