"""
Модуль: schemas.ulid

Модуль содержит Pydantic схему, используемую для представления ULID идентификатора в системе управления посылками.
ULID (Universally Unique Lexicographically Sortable Identifier) предоставляет компактный формат уникального
идентификатора, который включает в себя временную метку для естественной сортировки.

Содержит следующую схему:

    ULIDSchema: Схема для валидации и представления уникального идентификатора посылки в формате ULID.

"""

from pydantic import BaseModel, Field

class ULIDSchema(BaseModel):
    """
    Pydantic схема для представления ULID идентификатора посылки.

    Attributes:
        id (str): Уникальный идентификатор посылки в формате ULID, должен быть строкой длиной 26 символов.
    """

    id: str = Field(
        ...,
        min_length=26,
        max_length=26,
        description="Уникальный идентификатор посылки в формате ULID, должен быть строкой длиной 26 символов.",
        examples=["01ARZ3NDEKTSV4RRFFQ69G5FAV"]
    )