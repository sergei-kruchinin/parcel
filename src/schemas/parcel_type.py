"""
Модуль: schemas.parcel_type

Модуль содержит Pydantic схему для работы с типами посылок в системе.
Эта схема используется для обработки и валидации данных, связанных с типами посылок.

Содержит схему:

    ParcelTypeSchema: Схема, представляющая тип посылки, включая уникальный идентификатор и имя типа.
"""

from pydantic import BaseModel, Field


class ParcelTypeSchema(BaseModel):
    id: int = Field(...,
        description="Уникальный идентификатор типа посылки.",
        examples=[1])
    name: str = Field(..., min_length=3, max_length=50,
        description="Имя типа посылки, уникально и не более 50 символов.",
        examples=["Одежда"])
