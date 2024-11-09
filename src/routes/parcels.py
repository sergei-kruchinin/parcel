"""
Модуль: routes.parcels

Определяет маршруты для обработки запросов, связанных с посылками.


Маршруты:

    /api/parcels/
        Простая заглушка для получения всех типов посылок из базы данных.
        Выполняет выборку всех записей из таблицы типов посылок и возвращает их названия.
        Реализовано на скорую руку пока напрямую, сервис будет реализован позднее.
"""

import logging
from typing import List
from uuid import UUID

import ulid
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.parcel import ParcelCreateSchema, ParcelSchema
from .dependencies import get_db, get_user_session
from models.parcel import ParcelModel, ParcelTypeModel

logger = logging.getLogger(__name__)
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)


router = APIRouter()



@router.post("/", response_model=ParcelSchema, summary="Создать новую посылку",
             description="Создание новой посылки. Данные принимаются в формате JSON и валидируются. "
                         "Успешно зарегистрированная посылка возвращает индивидуальный ULID в контексте сессии пользователя.")
async def create_parcel(parcel: ParcelCreateSchema,
                        db: AsyncSession = Depends(get_db),
                        user_session_id: UUID = Depends(get_user_session)):
    # TODO создание посылки

    return {}  # пока будет 500 так как схема не соответствует





@router.get("/", response_model=List[ParcelSchema], summary="Получить список своих посылок",
            description="Возвращает список всех посылок текущего пользователя, включая их типы и стоимость доставки. "
                        "Поддерживает пагинацию и фильтрацию по типу и факту наличия стоимости доставки.")
async def get_user_parcels(
        offset: int = 0,
        limit: int = 10,
        type_id: int | None = Query(None),
        has_delivery_cost: bool | None = Query(None),
        db: AsyncSession = Depends(get_db),
        user_session_id: UUID = Depends(get_user_session)
):
    # TODO получение списка посылок текущего пользователя
    return []


@router.get("/{parcel_id}/", response_model=ParcelSchema, summary="Получить данные о посылке по ID",
            description="Возвращает данные по конкретной посылке, включая название, вес, тип и стоимость.")
async def get_parcel(parcel_id: str, db: AsyncSession = Depends(get_db),
                     user_session_id: UUID = Depends(get_user_session)):
    # TODO  получение данных о посылке по её ID
    return {}
