"""
Модуль: routes.healthy

Определяет API-маршрут для проверки состояния healthy контейнера

Маршруты:
    - GET /api/healthy - возвращает статус Healthy.

"""

import logging

from fastapi import APIRouter, status

from schemas.statuses import HealthySchema
from exceptions.error_schemas import InternalServerErrorResponse

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

router = APIRouter()

@router.get(
    "",
    response_model=HealthySchema,
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": InternalServerErrorResponse,
        },
    },
    summary="Получить информацию о Healthy сервиса",
    description=(
        "Возвращает статус 200 Ok если сервис жив, дополнительно"
        "Healthy: Ok для ручной проверки."
    )
)
async def healthy() -> HealthySchema:
    """
    Для показателя здоровья
    """
    logger.info("Healthy route called")
    return HealthySchema()
