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
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession


from schemas.parcel_type import ParcelTypeResponseSchema
from services.parcel_type import ParcelTypeService
from exceptions.exceptions import ParcelDatabaseError, ParcelValidationError
from exceptions.error_schemas import InternalServerErrorResponse
from .dependencies import get_db


logger = logging.getLogger(__name__)
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

router = APIRouter()

@router.get("/",
            response_model=List[ParcelTypeResponseSchema],
            responses={
                status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": InternalServerErrorResponse},
            },
            summary="Получить все типы посылок",
            description="Возвращает список всех типов посылок и их ID из отдельной таблицы в базе данных.")
async def get_parcel_types(db: AsyncSession = Depends(get_db)) -> List[ParcelTypeResponseSchema]:

    try:
        result = await ParcelTypeService.get_parcel_types(db=db)
        return result

    except ParcelValidationError as e:  # ошибка внутри бизнес-логики, потому 500, а не 422
        logger.exception(f"Ошибка в данных типов посылки: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Внутренняя ошибка сервера")

    except ParcelDatabaseError as e:
        logger.exception(f"Ошибка базы данных при запросе типов посылок: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Внутренняя ошибка сервера")

    except Exception as e:
        logger.exception(f"Неизвестная ошибка при запросе типов посылок для сессии: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Неизвестная ошибка")