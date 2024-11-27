"""
Модуль: models.parcel

Содержит определение ORM-модели посылки для работы с базой данных с
использованием SQLAlchemy.

Атрибуты класса:
    id (String(26)): ULID идентификатор посылки, строка длиной 26 символов.
        ULID является компактным идентификатором, который обеспечивает
        естественную сортировку благодаря встроенной временной метке.
        Пример: "01ARZ3NDEKTSV4RRFFQ69G5FAV";

    name (String(255)): Имя отправления, строка длиной до 255 символов.
        Пример: "Платье белое в горошек";

    weight (Decimal(8, 3)): Вес посылки в килограммах.
        Формат: XXXXX.XXX, максимум 99 999.999 кг.
        Пример: 0.200;

    value (Decimal(9, 2)): Стоимость содержимого посылки в долларах.
        Формат: XXXXXXX.XX, максимум: 9 999 999.99.
        Пример: 100.00;

    user_session_id (UUID): UUID идентификатор сессии пользователя.
        Хранится как бинарная строка длиной 16 байт. Отслеживает сессию
        пользователя в приложении.
        Пример UUID: '123e4567-e89b-12d3-a456-426614174000';

    shipping_cost (Decimal(9, 2) | None): Стоимость доставки в рублях.
        Может быть None, если не рассчитана.
        Формат: XXXXXXX.XX.
        Пример: 107.80;

    parcel_type_id (Int): Идентификатор типа посылки, внешний ключ для
        модели ParcelTypeModel.
        Пример: 1;
"""

from sqlalchemy import Column, ForeignKey, String, Integer, DECIMAL
from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType
from decimal import Decimal

from .base import Base
from .parcel_type import ParcelTypeModel  # type: ignore


class ParcelModel(Base):
    """
    ORM-модель для посылки.

    Attributes:
        id (str): Уникальный ULID идентификатор посылки.
        name (str): Название посылки.
        weight (Decimal): Вес посылки в килограммах.
        value (Decimal): Стоимость содержимого посылки в долларах.
        user_session_id (UUID): UUID (binary) идентификатор сессии пользователя.
        shipping_cost (Decimal | None): Стоимость доставки посылки.
        parcel_type_id (int): Идентификатор типа посылки.
        parcel_type (ParcelTypeModel): Связь с моделью ParcelTypeModel.
    """

    __tablename__ = 'parcels'

    id = Column(
        String(26),  # ULID хранится как строка длиной 26 символов
        primary_key=True,
        nullable=False,
        doc=(
            "Уникальный идентификатор посылки, в формате ULID, "
            "хранится как строка"
        )
    )

    name = Column(
        String(255),
        index=True,
        nullable=False,
        doc="Название посылки"
    )

    weight = Column(
        DECIMAL(precision=8, scale=3),
        nullable=False,
        doc="Вес посылки в килограммах"
    )

    value = Column(
        DECIMAL(precision=9, scale=2),
        nullable=False,
        doc="Стоимость содержимого посылки в долларах"
    )

    user_session_id = Column(
        UUIDType(binary=True),
        nullable=False,
        index=True,
        doc="Идентификатор сессии пользователя, UUID"
    )

    shipping_cost = Column(
        DECIMAL(precision=9, scale=2),
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
