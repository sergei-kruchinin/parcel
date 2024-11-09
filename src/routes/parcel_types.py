"""
Модуль: routes.parcel_types

Определяет маршруты для обработки запросов, связанных с посылками.
На данный момент, содержит базовую проверку работы с данными типов посылок из базы данных - для проверки
сборки контейнеров.

Маршруты:

    /api/parcel-types (get_parcel_types):
        Простая заглушка для получения всех типов посылок из базы данных.
        Выполняет выборку всех записей из таблицы типов посылок и возвращает их названия.
        Реализовано на скорую руку пока напрямую, сервис будет реализован позднее.
"""

import logging
from uuid import UUID
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Cookie
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from schemas.parcel_type import ParcelTypeSchema
from models.parcel_type import ParcelTypeModel
from .dependencies import get_db, get_user_session

logger = logging.getLogger(__name__)
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

router = APIRouter()

@router.get("/", response_model=List[ParcelTypeSchema], summary="Получить все типы посылок",
            description="Возвращает список всех типов посылок и их ID из отдельной таблицы в базе данных.")
async def get_parcel_types(db: AsyncSession = Depends(get_db), user_session_id: UUID = Depends(get_user_session)):

    logger.info("Get parcel types CALLED")
    logger.info(f"user_session_id: {user_session_id}")

    # TODO: вынести логику работы с БД в сервис
    try:
        result = await db.execute(select(ParcelTypeModel))
        parcel_types = result.scalars().all()

        return [parcel_type.name for parcel_type in parcel_types]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))