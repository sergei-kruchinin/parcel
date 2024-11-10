"""
Модуль: schemas.parcel

Содержит схемы Pydantic для работы с данными о посылках в системе.
Предоставляет базовые и расширенные схемы для создания, обработки и отображения информации о посылках.

Содержит схемы:
    ParcelBaseSchema: Базовая схема для представления основной информации о посылке, включая название,
        вес, тип и стоимость.
    ParcelRegisterSchema: Схема для создания новой посылки, основанная на ParcelBaseSchema.
    ParcelReceivedSchema: Схема для представления данных принятой посылки с использованием ULID.
    ParcelSchema: Расширенная схема, включающая полную информацию о посылке, включая идентификаторы
        сессии пользователя и стоимость доставки.
    ParcelResponseSchema: Схема, используемая для ответа, содержащая все данные о посылке,
        включая имя типа посылки.
"""

from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel, Field

from .ulid import ULIDSchema

class ParcelBaseSchema(BaseModel):
    """
    Базовая схема для представления информации о посылке.

    Attributes:

        name (str): Название посылки, не менее 3 и более 255 символов,
        weight (Decimal): Вес посылки в килограммах (макс. 8 цифр, из них 3 после точки), должен быть положительным,
        parcel_type_id (int): Идентификатор типа посылки,
        value (Decimal): Стоимость содержимого посылки в долларах (макс. 9 цифр, из них 2 после точки),
            должна быть положительной.
    """

    name: str = Field(..., min_length=3, max_length=255,
        description="Название посылки, не более 255 символов.",
        examples=["Платье белое в горошек"])
    weight: Decimal = Field(...,
        max_digits=8,
        decimal_places=3,
        gt=0,
        description="Вес посылки в килограммах, должен быть положительным.",
        examples=[0.2])
    parcel_type_id: int = Field(...,
        description="Идентификатор типа посылки.",
        examples=[1])
    value: Decimal = Field(...,
        max_digits=9,
        decimal_places=2,
        gt=0,
        description="Стоимость содержимого посылки в долларах, должна быть положительной.",
        examples=[100.0])


class ParcelRegisterSchema(ParcelBaseSchema):
    """
    Pydantic схема для регистрации посылки

    Attributes:

        name (str): Название посылки, не менее 3 и более 255 символов,
        weight (Decimal): Вес посылки в килограммах (макс. 8 цифр, из них 3 после точки), должен быть положительным,
        parcel_type_id (int): Идентификатор типа посылки,
        value (Decimal): Стоимость содержимого посылки в долларах (макс. 9 цифр, из них 2 после точки),
            должна быть положительной.
    """
    pass




class ParcelReceivedSchema(ULIDSchema):
    """
    Pydantic схема для ответа о приеме посылки.

    Выдает только id посылки в формате ULID, больше ничего.

    Attributes:

            id (str): Уникальный идентификатор посылки в формате ULID, должен быть строкой длиной 26 символов.
    """
    pass


class ParcelSafeSchema(ParcelBaseSchema, ULIDSchema):
    """
    Схема для обработки полной информации о посылке. Без информации о пользовательской сессии


    Attributes:

        name (str): Название посылки, не менее 3 и более 255 символов,
        weight (Decimal): Вес посылки в килограммах (макс. 8 цифр, из них 3 после точки), должен быть положительным,
        parcel_type_id (int): Идентификатор типа посылки,
        value (Decimal): Стоимость содержимого посылки в долларах (макс. 9 цифр, из них 2 после точки),
            должна быть положительной,
        id (str): Уникальный идентификатор посылки в формате ULID, должен быть строкой длиной 26 символов,
        shipping_cost (Decimal|None): Стоимость доставки посылки, в рублях, если рассчитана. Может быть None.
    """



    shipping_cost: Decimal | None = Field(
        None,
        max_digits=9,
        decimal_places=2,
        gt=0,
        description="Стоимость доставки посылки, если рассчитана. Может быть None."
    )


class ParcelSchema(ParcelSafeSchema):
    """
    Схема для обработки полной информации о посылке.

    Attributes:

        name (str): Название посылки, не менее 3 и более 255 символов,
        weight (Decimal): Вес посылки в килограммах (макс. 8 цифр, из них 3 после точки), должен быть положительным,
        parcel_type_id (int): Идентификатор типа посылки,
        value (Decimal): Стоимость содержимого посылки в долларах (макс. 9 цифр, из них 2 после точки),
            должна быть положительной,
        id (str): Уникальный идентификатор посылки в формате ULID, должен быть строкой длиной 26 символов,
        user_session_id (UUID): UUID идентификатор сессии пользователя,
        shipping_cost (Decimal|None): Стоимость доставки посылки, в рублях, если рассчитана. Может быть None.
    """

    user_session_id: UUID = Field(
        ...,
        description="UUID идентификатор сессии пользователя.",
        examples=["123e4567-e89b-12d3-a456-426614174000"]
    )

class ParcelResponseSchema(ParcelSafeSchema):
    """
    Схема для представления полной информации о посылке.

    Основана на безопасной схеме, не предоставляет информацию о пользовательской сессии

    Attributes:

        name (str): Название посылки, не более 255 символов,
        weight (Decimal): Вес посылки в килограммах (макс. 8 цифр, из них 3 после точки), должен быть положительным,
        parcel_type_id (int): Идентификатор типа посылки,
        value (Decimal): Стоимость содержимого посылки в долларах (макс. 9 цифр, из них 2 после точки),
            должна быть положительной,
        id (str): Уникальный идентификатор посылки в формате ULID, должен быть строкой длиной 26 символов,
        shipping_cost (Decimal|None|Str): Стоимость доставки посылки, в рублях, если рассчитана. Может быть None.
            Также, если не рассчитано, может быть указано "Не рассчитано"
        parcel_type_name (str): Имя типа посылки, уникально, не менее 3-х и не более 50 символов.
    """

    parcel_type_name: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description="Имя типа посылки, уникально и не более 50 символов.",
        examples=["Одежда"]
    )

    shipping_cost: Decimal | None | str = Field(
        "Не рассчитано",
        description="Стоимость доставки посылки, если рассчитана. Может быть \"не рассчитана\""
    )