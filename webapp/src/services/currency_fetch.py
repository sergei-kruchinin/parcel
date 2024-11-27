"""
Модуль: services.currency_fetch

Назначение:
    Предоставляет функциональность для получения курса доллара с удаленного API, указанного в `USD_EXCHANGE_API_URL`.

Ключевые особенности:
    - Использует асинхронный HTTP-клиент для выполнения запросов.
    - Преобразует данные из ответа API в значение `Decimal`.
    - Логирует ошибки и предоставляет механизм для обработки исключений.

Зависимости:
    - httpx: для выполнения HTTP-запросов.
    - decimal: для работы с денежными значениями.
    - logging: для логирования.
    - config.pricing_conf: содержит конфигурацию URL для API.
"""

import httpx
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
import logging

from config.pricing_conf import USD_EXCHANGE_API_URL


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class CurrencyFetchService:
    """
       Сервис для получения курса доллара с удаленного API.

       Методы:
           - fetch_currency_rate: Асинхронный метод для получения курса доллара.

       """
    @staticmethod
    async def fetch_currency_rate(api_url : str | None = USD_EXCHANGE_API_URL) -> Decimal:
        """
        Асинхронно получает курс доллара из указанного URL.

        Args:
            api_url (str, optional): URL API для получения курса доллара.
                По умолчанию берется значение из конфигурации `USD_EXCHANGE_API_URL`.

        Returns:
            Decimal: Значение курса доллара в формате Decimal.

        Raises:
            httpx.HTTPStatusError: Если API возвращает ошибочный HTTP-статус.
            httpx.RequestError: Если возникает ошибка при выполнении HTTP-запроса.
            decimal.InvalidOperation: Если ответ API не удалось преобразовать в Decimal.
        """

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(api_url)
                response.raise_for_status()
                data = response.json()
                rate = Decimal(data['Valute']['USD']['Value'])
                rate = rate.quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP)
                return rate
        except httpx.HTTPStatusError as e:
            logger.exception(f"HTTP ошибка: {e.response.status_code}")
            raise
        except httpx.RequestError as e:
            logger.exception(f"Ошибка при выполнении запроса: {e}")
            raise
        except InvalidOperation as e:
            logger.exception(f"Ошибка преобразования в Decimal: {e}")
            raise
        except Exception as e:
            print(f"Неожиданная ошибка: {e}")
            raise
