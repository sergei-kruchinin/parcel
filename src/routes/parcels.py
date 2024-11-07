"""
Модуль: routes.parcels

Определяет маршруты для обработки запросов, связанных с посылками.
На данный момент, содержит базовую проверку работы с данными типов посылок из базы данных - для проверки
сборки контейнеров.

Маршруты:

    /api/parcels/types (get_parcel_types):
        Простая заглушка для получения всех типов посылок из базы данных.
        Выполняет выборку всех записей из таблицы типов посылок и возвращает их названия.
        Реализовано на скорую руку пока напрямую, сервис будет реализован позднее.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.base import AsyncSessionLocal
from models.parcel_type import ParcelTypeModel

# пока оставим здесь
async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session

router = APIRouter()

@router.get("/types")
async def get_parcel_types(db: AsyncSession = Depends(get_db)):
    """ Простая заглушка, чтобы убедиться, что все работает. """
    try:
        result = await db.execute(select(ParcelTypeModel))
        parcel_types = result.scalars().all()

        return [parcel_type.name for parcel_type in parcel_types]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))