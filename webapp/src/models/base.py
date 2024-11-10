
"""
Модуль: models.base

Инициализирует асинхронную работу с базой данных с использованием SQLAlchemy и Aiomysql.

Переменные окружения, необходимые для работы:
- DATABASE_HOST: Хост базы данных.
- MYSQL_DATABASE: Имя базы данных.
- MYSQL_USER: Имя пользователя для подключения к базе данных.
- MYSQL_PASSWORD: Пароль пользователя для подключения.

Объекты для импорта:
    `Base`: для создания ORM-моделей.
    `DATABASE_CREDS`: для получения DATABASE_URL в Alembic (для синхронной работы с БД).
"""

import os
from sqlalchemy.ext.declarative import declarative_base
import logging

logger = logging.getLogger(__name__)

Base = declarative_base()

DATABASE_HOST = os.getenv("DATABASE_HOST")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
DATABASE_CREDS = f"{MYSQL_USER}:{MYSQL_PASSWORD}@{DATABASE_HOST}/{MYSQL_DATABASE}"
logger.info(f"From base.py: {DATABASE_CREDS}")
DATABASE_URL = f"mysql+aiomysql://{DATABASE_CREDS}"




