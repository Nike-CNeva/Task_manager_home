from fastapi import FastAPI
import uvicorn
from fastapi.staticfiles import StaticFiles
from routers import users, tasks, files, comments, auth, home
from settings import settings
from middlewares.auth_middleware import AuthMiddleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.models import APIKey, APIKeyIn, SecuritySchemeType
from fastapi.openapi.utils import get_openapi

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
           
# Переопределим схему OpenAPI, чтобы добавить авторизацию
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="My API",
        version="1.0.0",
        description="Документация с авторизацией",
        routes=app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }

    # По умолчанию применяем BearerAuth ко всем ручкам
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method.setdefault("security", [{"BearerAuth": []}])

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)