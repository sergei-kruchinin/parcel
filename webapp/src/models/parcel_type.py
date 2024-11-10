"""
Модуль: models.parcel_type

Содержит определение ORM-модели посылки для типов посылок.
Таблица должна быть заполнена перед обращением к маршрутам приложения.
Для тестовых целей заполнение данных осуществляется через миграции с использованием Alembic.
"""

from sqlalchemy import Column, Integer, String
from .base import Base


class ParcelTypeModel(Base):
    """
    Модель типа посылки для хранения в БД

    Attributes:
        id: Уникальный идентификатор типа посылки,
        name: Имя типа посылки, уникально для каждого типа.
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