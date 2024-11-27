"""
Модуль: routes.parcel_types

Определяет API-маршрут для получения типов посылок.
Использует сервис ParcelTypeService для асинхронной выборки данных из базы данных.

Маршруты:
    - GET /api/parcels-types - возвращает список всех типов посылок с их ID и названиями.

"""

import logging
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

def get_parcel_type_service(db: AsyncSession = Depends(get_db)) -> ParcelTypeService:
    """
    Получение экземпляра сервиса ParcelTypeService.

    Args:
        db (AsyncSession): Асинхронная сессия работы с базой данных.

    Returns:
        ParcelTypeService: Сервис для работы с типами посылок.
    """
    return ParcelTypeService(db=db)

@router.get(
    "/",
    response_model=List[ParcelTypeResponseSchema],
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": InternalServerErrorResponse,
        },
    },
    summary="Получить все типы посылок",
    description=(
        "Возвращает список всех типов посылок и их ID из отдельной таблицы "
        "в базе данных."
    )
)
async def get_parcel_types(
    parcel_type_service: ParcelTypeService = Depends(get_parcel_type_service)
) -> List[ParcelTypeResponseSchema]:
    try:
        result = await parcel_type_service.get_parcel_types()
        return result

    except ParcelValidationError as e:
        logger.error(f"Ошибка в данных типов посылки: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Внутренняя ошибка сервера"
        )

    except ParcelDatabaseError as e:
        logger.error(f"Ошибка базы данных при запросе типов посылок: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Внутренняя ошибка сервера"
        )

    except Exception as e:
        logger.error(f"Неизвестная ошибка при запросе типов посылок: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Неизвестная ошибка"
        )
