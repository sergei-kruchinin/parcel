"""
Модуль: services.currency_service

Назначение:
    Предоставляет сервис для работы с курсом доллара:
    - Получение курса из Redis.
    - Обновление курса доллара с удаленного API и сохранение его в Redis.

Особенности:
    - Использует асинхронные вызовы для работы с Redis и API.
    - Инкапсулирует бизнес-логику работы с валютами.

Зависимости:
    - services.currency_redis: Для взаимодействия с Redis.
    - services.currency_fetch: Для получения курса доллара с удаленного API.
    - config.pricing_conf: Конфигурация, содержащая настройки API и Redis.
"""

import logging
from decimal import Decimal

from services.currency_redis import CurrencyRedisService
from services.currency_fetch import CurrencyFetchService
from config.pricing_conf import USD_EXCHANGE_API_URL, USD_EXCHANGE_CACHE_EXPIRE
from interfaces.cache import ICacheService

logger = logging.getLogger(__name__)


class CurrencyService:
    """
    Сервис для работы с курсом доллара.

    Назначение:
        - Получение курса USD к RUB из Redis.
        - Обновление курса USD к RUB с удаленного API и сохранение его в Redis.

    Методы:
        - update_usd_rate: Обновляет курс доллара, получая данные из API.
        - get_usd_rate: Возвращает курс доллара из Redis, при необходимости обновляет его.
    """

    @staticmethod
    async def update_usd_rate(redis_wrapper: ICacheService) -> None:
        """
        Обновляет курс доллара в Redis.

        Args:
            redis_wrapper (ICacheService): Экземпляр обертки для взаимодействия с Redis.

        Raises:
            ValueError: Если API не возвращает данные о курсе валют.
            RuntimeError: Если возникает ошибка при обновлении курса.
        """
        try:
            rate = await CurrencyFetchService.fetch_currency_rate(USD_EXCHANGE_API_URL)
            if not rate:
                raise ValueError("API не вернул данные о курсе валют.")

            pricing_currency = CurrencyRedisService(redis_wrapper)
            await pricing_currency.set_usd_rub(rate, USD_EXCHANGE_CACHE_EXPIRE)
            logger.info(f"Курс доллара успешно обновлен: {rate}")

        except Exception as e:
            logger.error(f"Ошибка при обновлении курса доллара: {e}")
            raise RuntimeError(f"Ошибка при обновлении курса доллара: {e}")

    @staticmethod
    async def get_usd_rate(redis_wrapper: ICacheService) -> Decimal:
        """
        Получает курс доллара из Redis. Если курс отсутствует, инициирует его обновление.

        Args:
            redis_wrapper (ICacheService): Экземпляр обертки для взаимодействия с Redis.

        Returns:
            Decimal: Курс доллара, полученный из Redis или обновленный.

        Raises:
            ValueError: Если курс недоступен даже после обновления.

        """
        pricing_currency = CurrencyRedisService(redis_wrapper)
        usd_to_rub = await pricing_currency.get_usd_rub()
        if not usd_to_rub:
            logger.info("Курс валюты отсутствует в Redis, обновляем...")
            await CurrencyService.update_usd_rate(redis_wrapper)
            usd_to_rub = await pricing_currency.get_usd_rub()
            if not usd_to_rub:
                raise ValueError("Курс валют недоступен даже после обновления.")
        return usd_to_rub
