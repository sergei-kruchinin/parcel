"""
Модуль: models.parcel

Содержит определение ORM-модели посылки для работы с базой данных с использованием SQLAlchemy.

Комментарии, почему выбран UUID для ID посылки, UUID для ID сессии, и почему
выбрано хранение ID сессии, а не USER ID будут добавлен позднее.
"""

from sqlalchemy import Column, Float, ForeignKey, String, Integer
from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType
from .base import Base
from .parcel_type import ParcelTypeModel  # type: ignore
import uuid


class ParcelModel(Base):
    """
    Модель посылки для хранения в БД.

    Attributes:
        id: Уникальный идентификатор посылки,
        name: Название посылки,
        weight: Вес посылки в килограммах,
        value: Стоимость содержимого посылки в долларах,
        user_session_id: Идентификатор сессии пользователя,
        shipping_cost: Стоимость доставки,
        parcel_type_id: Идентификатор типа посылки,
        parcel_type: Связь с моделью ParcelTypeModel.
    """

    __tablename__ = 'parcels'

    id = Column(
        UUIDType(binary=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
        doc="Уникальный идентификатор посылки, генерируется автоматически"
    )

    name = Column(
        String(255),
        index=True,
        nullable=False,
        doc="Название посылки"
    )

    weight = Column(
        Float,
        nullable=False,
        doc="Вес посылки в килограммах"
    )

    value = Column(
        Float,
        nullable=False,
        doc="Стоимость содержимого посылки в долларах"
    )

    user_session_id = Column(
        UUIDType(binary=True),
        nullable=False,
        index=True,
        doc="Идентификатор сессии пользователя, по которой отслеживается посылка"
    )

    shipping_cost = Column(
        Float,
        nullable=True,
        doc="Стоимость доставки посылки (может отсутствовать)"
    )

    parcel_type_id = Column(
        Integer,
        ForeignKey('parcel_types.id'),
        nullable=False,
        doc="Идентификатор типа посылки, связанное поле"
    )

    parcel_type = relationship(
        "ParcelTypeModel",
        doc="Объект, представляющий тип посылки, связь с ParcelTypeModel"
    )