"""
Модуль: exceptions.error_handlers

Модуль обработки пользовательских исключений в приложении FastAPI.
Регистрируем обработчики ошибок, чтобы преобразовать исключения в
ответы JSON с соответствующими статус-кодами и сообщениями.
"""

from fastapi import FastAPI, Request, HTTPException
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.responses import JSONResponse
import logging

logger = logging.getLogger(__name__)

def register_http_error_handlers(app: FastAPI) -> None:
    """
    Регистрация обработчиков HTTP исключений для приложения FastAPI.

    Добавляет обработчики для стандартных HTTP исключений, генерируя
    JSON-ответы с соответствующими статус-кодами и деталями ошибки.

    Args:
        app (FastAPI): Экземпляр приложения FastAPI, к которому будут привязаны обработчики ошибок.
    """

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        """Обработчик для общих HTTP исключений."""
        logger.error(f"HTTP error occurred: {exc.detail}. Path: {request.url.path}")
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "detail": exc.detail,
                "path": request.url.path
            }
        )

    @app.exception_handler(StarletteHTTPException)
    async def starlette_http_exception_handler(request: Request, exc: StarletteHTTPException):
        """Обработчик для Starlette HTTP исключений."""
        logger.error(f"Starlette HTTP error occurred: {exc.detail}. Path: {request.url.path}")
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "detail": exc.detail,
                "path": request.url.path
            }
        )

    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception):
        """Обработчик для необработанных исключений."""
        logger.exception(f"Unhandled error occurred.  {str(exc)}. Path: {request.url.path}")
        return JSONResponse(
            status_code=500,
            content={
                "detail": "Внутренняя ошибка сервера",  # exc не передаем наружу, смотрим в логах
                "path": request.url.path
            }
        )

# Наши собственные обработчики для конкретных HTTP ошибок:

    @app.exception_handler(401)
    async def unauthorized_exception_handler(request: Request, exc: HTTPException):
        """Обработчик для 401 Unauthorized ошибок."""
        logger.warning(f"Unauthorized request. Path: {request.url.path}")
        return JSONResponse(
            status_code=401,
            content={
                "detail": exc.detail or "Пользовательская сессия не установлена",
                "path": request.url.path
            }
        )

    @app.exception_handler(400)
    async def bad_request_exception_handler(request: Request, exc: HTTPException):
        """Обработчик для 400 Bad Request ошибок."""
        logger.error(f"Bad request. Path: {request.url.path}")
        return JSONResponse(
            status_code=400,
            content={
                "detail": exc.detail or "Ошибка запроса",
                "path": request.url.path
            }
        )
    @app.exception_handler(404)
    async def not_found_exception_handler(request: Request, exc: HTTPException):
        """Обработчик для 404 Not Found ошибок."""
        logger.error(f"Not Found. Path: {request.url.path}")
        return JSONResponse(
            status_code=404,
            content={
                "detail": exc.detail or "Ресурс не найден",
                "path": request.url.path
            }
        )

    @app.exception_handler(500)
    async def internal_server_error_exception_handler(request: Request, exc: HTTPException):
        """Обработчик для 500 Internal Server Error ошибок."""
        logger.error(f"Internal server error. Path: {request.url.path}")
        return JSONResponse(
            status_code=500,
            content={
                "detail": exc.detail or "Внутренняя ошибка сервера",  # Подразумеваем, что в маршрутах уже
                                                                      # установлено безопасное сообщение
                                                                      # без выдачи внутренней информации наружу
                "path": request.url.path
            }
        )