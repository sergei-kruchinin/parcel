# Модуль: schemas.parcel_type

from pydantic import BaseModel, Field


class ParcelTypeSchema(BaseModel):
    id: int = Field(...,
                    description="Уникальный идентификатор типа посылки.",
                    examples=[1])
    name: str = Field(..., min_length=3, max_length=50,
                      description="Имя типа посылки, уникально и не более 50 символов.",
                      examples=["Одежда"])
