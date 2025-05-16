import os
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from backend.app.routers import users, tasks, files, comments, auth, home
from backend.app.core.settings import settings
#from backend.app.middlewares.auth_middleware import AuthMiddleware, get_password_hash
from fastapi.middleware.cors import CORSMiddleware

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
#app.add_middleware(AuthMiddleware)
#app.mount("/static", StaticFiles(directory="static", html=True), name="static")

# Подключение роутеров
app.include_router(home.router, tags=["Главная"])
app.include_router(users.router, tags=["Пользователи"])
app.include_router(tasks.router, tags=["Задачи"])
app.include_router(files.router, prefix="/files", tags=["Файлы"])
app.include_router(comments.router, prefix="/comments", tags=["Комментарии"])
app.include_router(auth.router, tags=["Авторизация"])

# Путь к фронтенду
frontend_dir = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

# Отдаём index.html по умолчанию
@app.get("/")
def serve_frontend():
    return FileResponse(os.path.join(frontend_dir, "index.html"))