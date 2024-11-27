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

import redis
import requests
from celery import Celery


# Константы

USD_EXCHANGE_INTERVAL  = int(os.getenv("USD_EXCHANGE_INTERVAL", 3600))  # Время обновления кэша курса в секундах (1 час)
SHIPPING_COST_UPDATE_INTERVAL = int(os.getenv("SHIPPING_COST_UPDATE_INTERVAL", 300))
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0")
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
CELERY_ENV = os.getenv("CELERY_ENV", "worker")
INTERNAL_SERVICES_URL = os.getenv("INTERNAL_SERVICES_URL")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Celery('tasks', broker=CELERY_BROKER_URL)
app.conf.broker_connection_retry_on_startup = True
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)


@app.task(bind=True, max_retries=3, default_retry_delay=60)
def update_exchange_rate(self):
    """
    Задача обновления курса валют. Пытается получить текущий курс USD к RUB из внешнего API и
    сохранить его в Redis. Повторяет попытку в случае временной неудачи.

    Args:
        self: Ссылка на объект задачи, позволяющая выполнять повторные попытки.
    """
    logger.info("Обращаемся к служебному роуту для обновления валюты")
    response = requests.post(f"{INTERNAL_SERVICES_URL}/api/update_usd_rate")
    if response.status_code == 200:
        logger.info("Успешно обновили курс доллара")
    else:
        logger.error(f"Не удалось обновить курс доллара {str(response.text)}")


@app.task
def update_shipping_costs():
    """
    Задача обновления стоимости доставки для всех посылок, у которых она еще не рассчитана.
    Использует курс USD к RUB, сохраненный в Redis, для выполнения вычислений.
    """
    logger.info("Обращаемся к служебному роуту для пересчета стоимостей доставки")
    response = requests.post(f"{INTERNAL_SERVICES_URL}/api/update_shipping_costs")
    if response.status_code == 200:
        logger.info("Успешно обновили стоимости доставки")
    else:
        logger.error(f"Не удалось обновить стоимости доставки {str(response.text)}")


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
