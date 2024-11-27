"""
Модуль: services.currency_redis

Назначение:
    Предоставляет методы для работы с курсом доллара (USD к RUB) в Redis.
    Служит для получения текущего курса и его сохранения с использованием обертки Redis.

Ключевые особенности:
    - Получение курса доллара из Redis.
    - Сохранение курса доллара в Redis с указанием времени жизни ключа.
    - Логирование успешных операций и ошибок.

Зависимости:
    - redis_wrapper: для работы с Redis.
    - decimal: для работы с денежными значениями.
    - config.pricing_conf: содержит конфигурацию ключей и времени жизни кэша.
"""

from decimal import Decimal, InvalidOperation
import logging
from config.pricing_conf import USD_EXCHANGE_CACHE_EXPIRE, USD_RUB_REDIS_KEY
from services.redis_wrapper import RedisWrapper
from interfaces.cache import ICacheService


# Настройка логирования
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class CurrencyRedisService:
    """
    Сервис для работы с курсом доллара в Redis.

    Методы:
        - get_usd_rub: Получает курс USD к RUB из Redis.
        - set_usd_rub: Сохраняет курс USD к RUB в Redis с указанием времени жизни.

    Attributes:
        redis_wrapper (RedisWrapper): Обертка для работы с Redis.

    """
    def __init__(self, redis_wrapper: ICacheService):
        """
        Инициализирует класс CurrencyRedisService с оберткой Redis.

        Args:
            redis_wrapper (ICacheService): Экземпляр обертки для Redis.
        """
        self.redis_wrapper = redis_wrapper

    async def get_usd_rub(self) -> Decimal | None:
        """
        Асинхронный метод для получения курса USD к RUB из Redis.

        Returns:
            Decimal | None: Курс USD к RUB, если значение существует, иначе None.

        В отличие от set_usd_rub в случае исключения не передает ее наверх, а возвращает None.
        Так удобнее обрабатывать
        """
        try:
            value = await self.redis_wrapper.get_value(USD_RUB_REDIS_KEY)
            if value is not None:
                rate = Decimal(value)
                logger.info("Курс USD к RUB успешно получен из Redis.")
                return rate
            logger.warning("Курс USD к RUB не найден в Redis.")
        except InvalidOperation as e:
            logger.error(f"Ошибка конвертации значения курса в Decimal: {e}")
        except Exception as e:
            logger.error(f"Ошибка при получении курса USD к RUB из Redis: {e}")
        return None

    async def set_usd_rub(self, value: Decimal, expire: int | None = USD_EXCHANGE_CACHE_EXPIRE) -> None:
        """
        Асинхронный метод для установки курса USD к RUB в Redis.

        Args:
            value (Decimal): Значение курса USD к RUB для сохранения.
            expire (int | None) : Время жизни ключа в секундах (по умолчанию 3600 секунд).

        Raises:
            :exception: если операция не завершилась успешно.

        """
        try:
            await self.redis_wrapper.set_value(USD_RUB_REDIS_KEY, str(value), expire)

            logger.info("Курс USD к RUB успешно сохранен в Redis.")
        except Exception as e:
            logger.error(f"Ошибка при сохранении курса USD к RUB в Redis: {e}")
            raise
