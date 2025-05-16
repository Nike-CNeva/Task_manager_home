from fastapi import FastAPI
#from fastapi.staticfiles import StaticFiles
from backend.app.database.database import Base, engine
from backend.app.models.user import User
from backend.app.routers import users, tasks, files, comments, auth, home
from backend.app.core.settings import settings
from backend.app.middlewares.auth_middleware import AuthMiddleware, get_password_hash
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
   
app = FastAPI(
    title="Система управления задачами для производства",
    description="API для управления задачами, пользователями, файлами и комментариями в производственной системе.",
    version="1.0",
    debug=settings.DEBUG
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
#app.mount("/static", StaticFiles(directory="static", html=True), name="static")

# Подключение роутеров
app.include_router(home.router, tags=["Главная"])
app.include_router(users.router, tags=["Пользователи"])
app.include_router(tasks.router, tags=["Задачи"])
app.include_router(files.router, prefix="/files", tags=["Файлы"])
app.include_router(comments.router, prefix="/comments", tags=["Комментарии"])
app.include_router(auth.router, tags=["Авторизация"])
           
@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Вызов создания админа
    async with AsyncSession(engine) as session:
        await create_admin(session)

async def create_admin(db: AsyncSession):

    
    admin = User(
        name="admin",
        username="admin",
        hashed_password=get_password_hash("Nike5427720"),  # должен быть хеш
        is_active=True,
        user_type="Администратор"
    )
    
    db.add(admin)
    await db.commit()
    print("Admin created")
