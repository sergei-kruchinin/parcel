import os

# Константы
USD_EXCHANGE_API_URL = os.getenv("USD_EXCHANGE_API_URL", "https://www.cbr-xml-daily.ru/daily_json.js")
USD_EXCHANGE_CACHE_EXPIRE = int(os.getenv("USD_EXCHANGE_INTERVAL", 3600))  # Время жизни кэша курса в секундах (1 час)
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))