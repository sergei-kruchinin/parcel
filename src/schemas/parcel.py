# Модуль: schemas.parcel

from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, constr, Field


class ParcelBaseSchema(BaseModel):
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


class ParcelCreateSchema(ParcelBaseSchema):
    pass


class ParcelSchema(ParcelBaseSchema):
    id: constr(min_length=26, max_length=26) = Field(
        ...,
        description="Уникальный идентификатор посылки в формате ULID, должен быть строкой длиной 26 символов.",
        examples=["01ARZ3NDEKTSV4RRFFQ69G5FAV"]
    )
    user_session_id: UUID = Field(...,
                                  description="UUID идентификатор сессии пользователя.",
                                  examples=["123e4567-e89b-12d3-a456-426614174000"]
                                  )
    shipping_cost: Decimal | None = Field(None,
                                          max_digits=9,
                                          decimal_places=2,
                                          gt=0,
                                          description="Стоимость доставки посылки, если рассчитана.")
