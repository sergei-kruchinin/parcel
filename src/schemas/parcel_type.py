"""
Модуль: schemas.parcel_type

Модуль содержит Pydantic схему для работы с типами посылок в системе.
Эта схема используется для обработки и валидации данных, связанных с типами посылок.

Содержит схемы:

    ParcelTypeSchema: Схема для представления типа посылки, включая уникальный идентификатор и имя типа.
    ParcelTypeResponseSchema: Схема для обеспечения безопасного использования данных о типах при отправке ответов.

"""

from pydantic import BaseModel, Field


class ParcelTypeSchema(BaseModel):
    """
    Схема Pydantic для типа посылки.

    Attributes:

        id (int): Уникальный идентификатор типа посылки,
        name (str): Имя типа посылки, уникально и длиной не более 50 символов.

    """

    id: int = Field(...,
        description="Уникальный идентификатор типа посылки.",
        examples=[1])
    name: str = Field(..., min_length=3, max_length=50,
        description="Имя типа посылки, уникально и не более 50 символов.",
        examples=["Одежда"])


# Чтобы быть уверенными, что мы используем схему, предназначенную точно для ответа, а не для внутреннего использования
class ParcelTypeResponseSchema(ParcelTypeSchema):
    """
    Схема Pydantic для предоставления ответа о типе посылки.

    Attributes:

        id (int): Уникальный идентификатор типа посылки,
        name (str): Имя типа посылки, уникально и длиной не более 50 символов.

    """
    pass