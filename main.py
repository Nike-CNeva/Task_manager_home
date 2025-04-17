from fastapi import FastAPI
import uvicorn
from fastapi.staticfiles import StaticFiles
from routers import users, tasks, files, comments, auth, home
from settings import settings
from middlewares.auth_middleware import AuthMiddleware
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
app.add_middleware(AuthMiddleware)
app.mount("/static", StaticFiles(directory="static", html=True), name="static")

# Подключение роутеров
app.include_router(home.router, tags=["Главная"])
app.include_router(users.router, tags=["Пользователи"])
app.include_router(tasks.router, tags=["Задачи"])
app.include_router(files.router, prefix="/files", tags=["Файлы"])
app.include_router(comments.router, prefix="/comments", tags=["Комментарии"])
app.include_router(auth.router, tags=["Авторизация"])
           

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)