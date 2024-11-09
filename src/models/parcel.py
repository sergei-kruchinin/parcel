"""
Модуль: models.parcel

Содержит определение ORM-модели посылки для работы с базой данных с использованием SQLAlchemy.

Выбор типов:
    id (String(26)): ULID идентификатор посылки. Хранится в виде строки.
                            ULID является более компактным, чем UUID, и предоставляет возможность естественной
                            сортировки благодаря встроенной временной метке.
                            ULID сохраняет свою уникальность и может быть безопасно
                            сгенерирован в разных системах, так как не нуждается в централизованной выдаче.
                            В отличие от id типа Integer, с ULID нельзя легко подобрать номер следующей или
                            предыдущей посылки, что важно для обеспечения безопасности публичных трекеров отправлений.
                            Пример: "01ARZ3NDEKTSV4RRFFQ69G5FAV"
    name (String(255)): Имя отправления. В целом до 255 символов длины хватит.
                            Пример: "Платье белое в горошек"
    weight (Decimal(8,3)): Вес посылки в килограммах. Формат XXXXX.XXX, т.е. max: 99 999.999
                            Нужны данные от бизнеса, какой максимум отправления, но я взял с запасом.
                            Груженая фура примерно 40 000 кг.
                            Вес с точностью в десятках грамм (два знака) был бы достаточен, но в некоторых
                            случаях (авиапочта) может быть с точностью до знака, потому выбрано 3 знака после точки.
                            Пример 0.2
    value (Decimal(9,2)): Стоимость содержимого посылки в долларах. Формат XXXXXXX.XX, т.е. max: 9 999 999.99
                            Груженая фура примерно 1 500 000 долларов.
                            Пример: 100
    user_session_id (UUID): UUID идентификатор сессии пользователя.
                            В базе данных хранится как бинарная строка длиной 16 байт.
                            Выбор UUID сессии для идентификации пользователя обусловлен условием задачи:
                            приложение не содержит авторизации, отслеживает пользователей
                            по сессии, т.е. у каждого пользователя свой список посылок.
                            Вероятно, стоило бы хранить user_id, но чтобы его извлечь нужно либо быть уверенным,
                            что используется jwt и у нас есть ключ (на самом деле нет), либо использовать быстрое
                            хранилища, например Redis, чтобы сопоставить `user_session_id` с `user_id`.
                            Можно предположить, что пользователь может начать оформлять посылки в принципе без
                            авторизации, а авторизация будет предложена позже (по идее эту логику можно было бы
                            вынести во фронтенд, с другой стороны, на бэкенде уже можно начать обработку посылки,
                            не дожидаясь регистрации). В таком случае другой сервис должен отслеживать
                            связь user_session_id с user_ud.
                            Для простоты тестирования будем считать, что user_session_id будет установлен не
                            в виде заголовка, а в cookie, тогда клиенту не нужно будет заботиться о постоянном
                            указании идентификатора сессии. В тестовых целях сами сгенерируем его в middleware
                            Пример UUID в читаемом формате: '123e4567-e89b-12d3-a456-426614174000'
    shipping_cost (Decimal(9,2)): Стоимость доставки, в рублях. Может быть не рассчитана (None).
                            Формат XXXXXXX.XX, т.е. max: 9 999 999.99
                            Пример: 107.8
    parcel_type_id (Int): Идентификатор типа посылки, из модели ParcelTypeModel.
                            Пример: 1

"""

from sqlalchemy import Column, ForeignKey, String, Integer, DECIMAL
from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType

from .base import Base
from .parcel_type import ParcelTypeModel  # type: ignore


class ParcelModel(Base):
    """
    Модель посылки для хранения в БД.

    Attributes:
        id: Уникальный идентификатор посылки (ULID),
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
        String(26),  # ULID хранится как строка длиной 26 символов
        primary_key=True,
        nullable=False,
        doc="Уникальный идентификатор посылки, в формате ULID, хранится как строка"
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