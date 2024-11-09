"""
Модуль: routes.dependencies

Зависимости
"""

import logging
from uuid import UUID

from fastapi import HTTPException, Cookie, status
from sqlalchemy.ext.asyncio import AsyncSession
from models.base import AsyncSessionLocal

logger = logging.getLogger(__name__)


async def get_db() -> AsyncSession:
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
        HTTPException: Ошибка 401, если cookie отсутствует
                       Ошибка 400, если user_session_id имеет некорректный формат.
    """

    if not user_session_id:
        logging.warning("Не предоставлен user_session_id cookie")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Пользовательская сессия не установлена")
    try:
        user_session_uuid = UUID(user_session_id)
        return user_session_uuid
    except ValueError as e:
        logging.error(f"Некорректный UUID: {user_session_id}, ошибка: {e}")
        # чтобы не путать со стандартной 422 ошибкой, для простоты будем возвращать 400
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Не верный формат ID сессии")
