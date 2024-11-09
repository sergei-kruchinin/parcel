"""
Модуль: app

Используется в Dockerfile для создания и запуска Docker контейнера.

"""

from fastapi import FastAPI, Request, Response
from uuid import uuid4, UUID
import logging
from routes import parcels
from routes import parcel_types
from exceptions.error_handlers import register_http_error_handlers




logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

app = FastAPI()

register_http_error_handlers(app)


@app.middleware("http")
async def add_user_session_id(request: Request, call_next):

    # Если нужно проверить как будет реагировать без установленной куки, если работаем через сваггер
    # раскомментировать:
    if request.url.path.startswith(("/docs", "/redoc", "/openapi.json")):
        return await call_next(request)

    # Получаем ID сессии из cookies запроса
    user_session_id = request.cookies.get('user_session_id')

    if user_session_id:
        # Если user_session_id в cookies есть, просто продолжаем обработку
        return await call_next(request)

    # Если user_session_id в cookies не установлена, сгенерируем UUID и установим в cookies
    # после получения ответа от FastAPI
    user_session_id = str(uuid4())
    response = await call_next(request)
    response.set_cookie(key="user_session_id", value=user_session_id, httponly=True)

    return response




@app.middleware("http")
async def log_request_headers(request: Request, call_next):
    """Логирование заголовков для отладки"""
    headers = request.headers
    logging.info("Request Headers: %s", headers)

    response = await call_next(request)
    return response

app.include_router(parcels.router, prefix="/api/parcels")
app.include_router(parcel_types.router, prefix="/api/parcel-types")
