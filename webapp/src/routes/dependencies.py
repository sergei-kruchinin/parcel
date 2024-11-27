"""
Модуль: routes.dependencies

Определяет зависимости для использования в маршрутах FastAPI, такие как подключение
к базе данных и проверка пользовательской сессии.
"""

import logging
from uuid import UUID

from fastapi import HTTPException, Cookie, status
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from models.base import DATABASE_URL

logger = logging.getLogger(__name__)

# Создание асинхронного движка для работы с базой данных
engine = create_async_engine(DATABASE_URL, future=True, echo=False)

# Создание фабрики сессий для работы с базой данных
AsyncSessionLocal = sessionmaker(  # type: ignore
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


async def get_db() -> AsyncSession:
    """
    Получение асинхронной сессии работы с базой данных.

    Yields:
        AsyncSession: Асинхронная сессия для выполнения операций с базой данных.
    """
    async with AsyncSessionLocal() as session:
        yield session


def get_user_session(user_session_id: str = Cookie(
    None,
    description="Сессия пользователя в формате UUID, только для примера (в Swagger не устанавливается)",
    example="123e4567-e89b-12d3-a456-426614174000"
)) -> UUID:
    """
    Получает UUID сессии пользователя из cookie.

    Args:
        user_session_id (str): Строка идентификатора сессии пользователя в формате UUID.

    Returns:
        UUID: Объект UUID, представляющий идентификатор сессии пользователя.

    Raises:
        HTTPException:
            Ошибка 401, если cookie отсутствует.
            Ошибка 400, если user_session_id имеет некорректный формат.
    """
    if not user_session_id:
        logger.warning("Не предоставлен user_session_id в cookie")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Пользовательская сессия не установлена"
        )

    try:
        user_session_uuid = UUID(user_session_id)
        return user_session_uuid
    except ValueError as e:
        logger.error(f"Некорректный UUID: {user_session_id}, ошибка: {e}")
        # чтобы не путать со стандартной 422 ошибкой, возвращаем 400
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Неверный формат ID сессии"
        )
