"""
Модуль: schemas.healthy

Модуль содержит Pydantic схему, используемую для ответа о healthy сервиса для Docker compose.

Содержит следующую схему:

    HealthySchema: Схема для ответа о healthy сервиса.

"""

from pydantic import BaseModel, Field

class HealthySchema(BaseModel):
    """
    Pydantic схема для ответа о healthy сервиса

    Attributes:
        healthy (str): Состояние (Ok)
    """

    healthy: str = Field(
        default="Ok",
        description="Сообщение, что сервис Healthy - Ok",
    )

class MessageSchema(BaseModel):
    """
    Pydantic схема для ответа о результате операции с сообщением

    Attributes:
        message (str): Описание успешного действия
    """

    message: str = Field(
        default="Операция успешно завершена",
        description="Сообщение об успешности операции",
    )