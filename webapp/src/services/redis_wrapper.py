"""
Модуль: services.redis_wrapper
Содержит обертку для работы с Redis и обработчики событий FastAPI для инициализации и завершения пула соединений Redis.
"""

import redis.asyncio as aioredis
from redis.asyncio.client import Redis
from redis.asyncio.connection import ConnectionPool
from typing import Optional
import logging


# Настройка логирования
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# --- Пул Соединений для Redis ---
redis_pool: ConnectionPool | None = None

async def initialize_redis_pool(host: str, port: int, max_connections: int):
    """
    Инициализация пула соединений Redis при старте приложения.

    Args:
        host (str): Хост для подключения к Redis.
        port (int): Порт для подключения к Redis.
        max_connections (int): Максимальное количество соединений в пуле.
    """
    global redis_pool
    try:
        redis_pool = aioredis.ConnectionPool.from_url(
            f"redis://{host}:{port}",
            encoding="utf-8",
            decode_responses=True,
            max_connections=max_connections
        )
        logger.info("Redis pool успешно инициализирован.")
    except Exception as e:
        logger.error(f"Ошибка при инициализации пула соединений Redis: {e}")
        raise

async def close_redis_pool():
    """
    Закрытие пула соединений Redis при завершении работы приложения.
    """
    if redis_pool:
        try:
            await redis_pool.disconnect(inuse_connections=True)
            logger.info("Redis pool успешно закрыт.")
        except Exception as e:
            logger.error(f"Ошибка при закрытии пула соединений Redis: {e}")

class RedisWrapper:
    def __init__(self):
        """
        Инициализирует класс RedisWrapper с пулом соединений Redis.
        """
        if redis_pool is None:
            logger.error("Redis pool has not been initialized.")
            raise ValueError("Redis pool has not been initialized.")
        self.redis = Redis(connection_pool=redis_pool)

    async def set_value(self, key: str, value: str, expire: int | None = None) -> None:
        """
        Асинхронный метод для установки значения в Redis.

        Args:
            key (str): Ключ для сохранения значения.
            value (str): Значение для сохранения.
            expire (int | None): Время жизни ключа в секундах (если указано).


        """
        try:
            await self.redis.set(key, value, ex=expire)
            logger.info(f"Значение для ключа '{key}' успешно сохранено в Redis.")
        except Exception as e:
            logger.error(f"Ошибка при записи значения в Redis для ключа '{key}': {e}")
            raise

    async def get_value(self, key: str) -> str | None:
        """
        Асинхронный метод для получения значения из Redis.

        Args:
            key (str): Ключ для получения значения.

        Returns:
            Optional[str]: Значение, сохраненное по ключу, или None, если ключ не найден.
        """
        try:
            value = await self.redis.get(key)
            if value is not None:
                logger.info(f"Значение для ключа '{key}' успешно получено из Redis.")
            else:
                logger.warning(f"Значение для ключа '{key}' не найдено в Redis.")
            return value
        except Exception as e:
            logger.error(f"Ошибка при получении значения из Redis для ключа '{key}': {e}")
            return None


