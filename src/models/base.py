
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
    `AsyncSessionLocal`: для создания асинхронных сессий работы с базой данных.
    `DATABASE_CREDS`: для получения DATABASE_URL в Alembic (для синхронной работы с БД).
"""
import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from databases import Database
import logging

logger = logging.getLogger(__name__)

Base = declarative_base()

DATABASE_HOST = os.getenv("DATABASE_HOST", "")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "")
MYSQL_USER = os.getenv("MYSQL_USER", "")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
DATABASE_CREDS = f"{MYSQL_USER}:{MYSQL_PASSWORD}@{DATABASE_HOST}/{MYSQL_DATABASE}"
logger.info(f"From base.py: {DATABASE_CREDS}")
DATABASE_URL = f"mysql+aiomysql://{DATABASE_CREDS}"



engine = create_async_engine(DATABASE_URL, future=True, echo=False)


AsyncSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)

database = Database(DATABASE_URL)


