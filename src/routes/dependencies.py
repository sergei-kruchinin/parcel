"""
Модуль: routes.dependencies

Зависимости
"""

import logging
from uuid import UUID

from fastapi import HTTPException, Cookie
from sqlalchemy.ext.asyncio import AsyncSession
from models.base import AsyncSessionLocal

logger = logging.getLogger(__name__)


# пока оставим здесь
async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session


def get_user_session(user_session_id: str = Cookie(
    None,
    description="Сессия пользователя в формате UUID, только для примера (в Swagger не устанавливается)",
    example="123e4567-e89b-12d3-a456-426614174000"
)) -> UUID:
    if not user_session_id:
        logging.warning("No user_session_id cookie provided")
        raise HTTPException(status_code=400, detail="User session ID missing")
    try:
        user_session_uuid = UUID(user_session_id)
        return user_session_uuid
    except ValueError as e:
        logging.error(f"Некорректный UUID: {user_session_id}, ошибка: {e}")
        raise HTTPException(status_code=400, detail="Invalid user session ID format")
