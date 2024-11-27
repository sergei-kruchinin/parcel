"""
Модуль: app

Предоставляет настройку и запуск веб-приложения FastAPI, используемого в Docker-контейнере.
Определяет и регистрирует middleware, маршруты и обработчики ошибок.

Функции:

1. add_user_session_id(request: Request, call_next):
   Middleware для добавления уникального идентификатора сессии пользователя (UUID) в cookies,
   если он ещё не установлен. Это обеспечивает идентификацию сессии пользователя.

2. log_request_headers(request: Request, call_next):
   Middleware для логирования заголовков HTTP-запросов для целей отладки. Все заголовки запроса
   записываются в журналы.

Маршруты:

- /api/parcels: Обработка запросов, связанных с посылками.
- /api/parcel-types: Обработка запросов, связанных с типами посылок.

Используемые зависимости:

- FastAPI: Основной фреймворк для построения приложения.
- uuid: Для генерации уникальных идентификаторов сессии пользователя.
- logging: Для создания логов и отладки.
- routes.parcels и routes.parcel_types: Определяют маршруты и обработку логики приложения.
- exceptions.error_handlers: Регистрация пользовательских обработчиков ошибок HTTP.
"""

from fastapi import FastAPI, Request, Response
from uuid import uuid4
import logging
from typing import Any
from routes import parcels
from routes import parcel_types
from routes import healthy
from exceptions.error_handlers import register_http_error_handlers




logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

app = FastAPI()

register_http_error_handlers(app)


@app.middleware("http")
async def add_user_session_id(request: Request, call_next: Any) -> Response:
    """
    Middleware для добавления уникального идентификатора сессии пользователя (UUID) в cookies.
    Если cookies не содержит 'user_session_id', генерирует новый UUID и устанавливает его.

    Args:
        request (Request): HTTP-запрос FastAPI.
        call_next (Any): Функция для вызова следующего middleware.

    Returns:
        Response: HTTP-ответ с установленным в cookies 'user_session_id', если он отсутствует.
    """

    # Если нужно проверить как будет реагировать без установленной cookie, если работаем через swagger
    # раскомментировать. Иначе после посещения /doc user_session_id уже будет установлена:
    # if request.url.path.startswith(("/docs", "/redoc", "/openapi.json")):
    #     return await call_next(request)

    # Получаем ID сессии из cookies
    user_session_id = request.cookies.get('user_session_id')

    # Если user_session_id в cookies есть, просто продолжаем обработку
    if user_session_id:
        return await call_next(request)

    # Если user_session_id в cookies не установлена, сгенерируем UUID и установим в cookies
    # после получения ответа от FastAPI
    user_session_id = str(uuid4())
    response = await call_next(request)
    response.set_cookie(key="user_session_id", value=user_session_id, httponly=True)

    return response


@app.middleware("http")
async def log_request_headers(request: Request, call_next: Any) -> Response:
    """
    Middleware для логирования заголовков HTTP-запросов.
    Для отладки.

    Args:
        request (Request): HTTP-запрос FastAPI.
        call_next (Any): Функция для вызова следующего middleware.

    Возвращает:
        Response: HTTP-ответ после логирования заголовков запроса.
    """

    headers = request.headers
    logging.info("Request Headers: %s", headers)

    response = await call_next(request)
    return response


app.include_router(parcels.router, prefix="/api/parcels")
app.include_router(parcel_types.router, prefix="/api/parcel-types")
app.include_router(healthy.router, prefix="/api/healthy")
