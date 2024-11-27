"""
Модуль: models.parcel_type

Содержит определение ORM-модели для хранения типов посылок.
Таблица должна быть заполнена перед использованием маршрутов приложения.
Для тестовых целей данные заполняются через миграции с использованием Alembic.
"""

from sqlalchemy import Column, Integer, String
from .base import Base


class ParcelTypeModel(Base):
    """
    Модель типа посылки для хранения в базе данных.

    Attributes:
        id (int): Уникальный идентификатор типа посылки;
        name (str): Имя типа посылки, уникальное для каждого типа.
    """

    __tablename__ = 'parcel_types'

    id = Column(
        Integer,
        primary_key=True,
        index=True,
        comment="Уникальный идентификатор типа посылки"
    )

    name = Column(
        String(50),
        unique=True,
        nullable=False,
        comment="Имя типа посылки, уникальное"
    )
