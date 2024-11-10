"""
Модуль: tasks

Модуль задач для обработки данных с использованием Celery.

Содержит задачи для периодического обновления курса валют и обновления стоимости доставки посылок
на основе этих курсов.

Так как celery не поддерживает асинхронные функции, чтобы не создавать оберток, сделал по-простому:
используем синхронные requests, redis и SQLAlchemy.

"""

import logging
import os
from decimal import Decimal, InvalidOperation

import redis
import requests
from celery import Celery
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker

from models.base import DATABASE_CREDS
from models.parcel import ParcelModel

# Константы
USD_EXCHANGE_API_URL = os.getenv("USD_EXCHANGE_API_URL", "https://www.cbr-xml-daily.ru/daily_json.js")
USD_EXCHANGE_CACHE_EXPIRE = int(os.getenv("USD_EXCHANGE_INTERVAL", 3600))  # Время жизни кэша курса в секундах (1 час)
USD_EXCHANGE_INTERVAL = USD_EXCHANGE_CACHE_EXPIRE  # Время обновления кэша курса в секундах (1 час)
SHIPPING_COST_UPDATE_INTERVAL = int(os.getenv("SHIPPING_COST_UPDATE_INTERVAL", 300))
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0")
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
CELERY_ENV = os.getenv("CELERY_ENV", "worker")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Celery('tasks', broker=CELERY_BROKER_URL)
app.conf.broker_connection_retry_on_startup = True
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)

# Создание синхронного движка и сессии
DATABASE_URL_SYNC = f"mysql+pymysql://{DATABASE_CREDS}"
sync_engine = create_engine(DATABASE_URL_SYNC, future=True, echo=False)
SessionLocal = sessionmaker(bind=sync_engine, expire_on_commit=False)


@app.task(bind=True, max_retries=3, default_retry_delay=60)
def update_exchange_rate(self):
    """
    Задача обновления курса валют. Пытается получить текущий курс USD к RUB из внешнего API и
    сохранить его в Redis. Повторяет попытку в случае временной неудачи.

    Args:
        self: Ссылка на объект задачи, позволяющая выполнять повторные попытки.
    """
    try:
        response = requests.get(USD_EXCHANGE_API_URL, timeout=10)
        response.raise_for_status()
        data = response.json()
        usd_rate = data['Valute']['USD']['Value']
        redis_client.set('usd_to_rub', str(usd_rate), ex=USD_EXCHANGE_CACHE_EXPIRE)
        logger.info("Курс валют обновлен и сохранен в Redis.")
    except requests.RequestException as e:
        logger.error(f"Ошибка при обращении к API для получения курса валют: {e}")
        if self.request.retries < self.max_retries:
            self.retry(exc=e)
    except redis.RedisError as e:
        logger.error(f"Ошибка при работе с Redis: {e}")
        if self.request.retries < self.max_retries:
            self.retry(exc=e)


@app.task
def update_shipping_costs():
    """
    Задача обновления стоимости доставки для всех посылок, у которых она еще не рассчитана.
    Использует курс USD к RUB, сохраненный в Redis, для выполнения вычислений.
    """
    try:
        usd_to_rub_bytes = redis_client.get('usd_to_rub')

        if usd_to_rub_bytes is None:
            logger.info("Курс валюты недоступен, пробуем вызвать обновление курса")
            update_exchange_rate.apply_async()
            raise ValueError("Курс валют отсутствует в Redis.")

        usd_to_rub = Decimal(usd_to_rub_bytes.decode('utf-8'))

        with SessionLocal() as session:
            result = session.execute(select(ParcelModel).filter(ParcelModel.shipping_cost.is_(None)))
            parcels = result.scalars().all()

            for parcel in parcels:
                weight = Decimal(parcel.weight)
                value = Decimal(parcel.value)
                new_shipping_cost = (weight * Decimal('0.5') + value * Decimal('0.01')) * usd_to_rub
                parcel.shipping_cost = new_shipping_cost

            session.commit()
        logger.info("Стоимость доставки обновлена для всех посылок без расчетной стоимости.")
    except (ValueError, InvalidOperation) as e:
        logger.error(f"Ошибка при расчете стоимости доставки: {e}")

    except SQLAlchemyError as e:
        logger.error(f"Ошибка при работе с БД: {e}")

    except redis.RedisError as e:
        logger.error(f"Ошибка при работе с Redis: {e}")

    except Exception as e:
        logger.error(f"Общая ошибка при обновлении стоимости доставки: {e}")


if CELERY_ENV == "beat":
    logger.info("Запускаем задачу получения валюты на старте")
    app.tasks['tasks.update_exchange_rate'].apply_async()


app.conf.beat_schedule = {
    'update-exchange-rate-every-hour': {
        'task': 'tasks.update_exchange_rate',
        'schedule': USD_EXCHANGE_INTERVAL  # 3600
    },
    'update-shipping-costs-every-5-minutes': {
        'task': 'tasks.update_shipping_costs',
        'schedule': SHIPPING_COST_UPDATE_INTERVAL  # 300
    },
}
