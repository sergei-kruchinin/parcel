"""
Модуль: routes.internal_services

Определяет API-маршруты для служебных модулей.

Пока не сделано:
    - Не сделана межсервисная авторизация
 """
import logging
from contextlib import asynccontextmanager

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from interfaces.cache import ICacheService
from exceptions.error_schemas import InternalServerErrorResponse
from services.redis_wrapper import RedisWrapper, initialize_redis_pool, close_redis_pool
from services.currency_service import CurrencyService
from services.shipping_costs_update_service import ShippingCostsUpdateService
from schemas.statuses import MessageSchema
from .dependencies import get_db
from config.pricing_conf import REDIS_HOST, REDIS_PORT, REDIS_MAX_CONNECTIONS

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

router = APIRouter()


@asynccontextmanager
async def lifespan(app):
    try:
        await initialize_redis_pool(REDIS_HOST, REDIS_PORT, max_connections=REDIS_MAX_CONNECTIONS)
        logger.info("Redis pool инициализирован при старте FastAPI приложения.")
        yield
    except Exception as e:
        logger.critical(f"Ошибка при инициализации Redis: {e}")
        raise RuntimeError("Не удалось инициализировать Redis.")
    finally:
        await close_redis_pool()
        logger.info("Redis pool закрыт при завершении работы FastAPI приложения.")


async def get_redis_wrapper() -> ICacheService:
    return RedisWrapper()


@router.post(
    "/update_usd_rate",
    response_model=MessageSchema,
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": InternalServerErrorResponse,
        },
    },
    summary="Обновить курс доллара",
    description="Служит для вызова из Celery",
)
async def update_usd_rate(redis_wrapper: ICacheService = Depends(get_redis_wrapper)) -> MessageSchema:
    """
    Обновляет курс доллара в Redis.
    """
    try:
        await CurrencyService.update_usd_rate(redis_wrapper)
        return MessageSchema(message="Курс доллара успешно обновлен")
    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post(
    "/update_shipping_costs",
    response_model=MessageSchema,
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": InternalServerErrorResponse,
        },
    },
    summary="Обновить цены доставки",
    description="Служит для вызова из Celery",
)
async def update_shipping_costs(
    redis_wrapper: RedisWrapper = Depends(get_redis_wrapper),
    db: AsyncSession = Depends(get_db)
) -> MessageSchema:
    """
    Обновляет стоимость доставки на основе актуального курса доллара.
    """
    try:
        usd_to_rub = await CurrencyService.get_usd_rate(redis_wrapper)
        logger.info(f"Используем курс USD/RUB: {usd_to_rub}")

        shipping_costs_update_service = ShippingCostsUpdateService(db)
        await shipping_costs_update_service.update_shipping_costs(usd_to_rub)

        logger.info("Стоимость доставки обновлена для всех посылок.")
        return MessageSchema(message="Стоимость доставки обновлена для всех посылок.")
    except ValueError as e:
        logger.warning(f"Ошибка получения курса валют: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Ошибка при обновлении стоимости доставки: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка при обновлении стоимости доставки."
        )
