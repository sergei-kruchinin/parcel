"""
Модуль: exceptions.error_schemas

Схемы Pydantic для обработки HTTP ошибок в API.

Используется только для Swagger, для простоты в error_handlers не используется.
Для удобства работы с исключениями помещен в exceptions, а не в schemas

"""
from pydantic import BaseModel, Field


class ErrorResponse(BaseModel):
    """
    Базовая схема для сообщений об ошибке

    Attributes:

        detail (str): Описание ошибки.
        path (str): Путь, в котором произошла ошибка.
    """
    detail: str = Field(..., description="Краткое описание ошибки.")
    path: str = Field(
        "Путь, в котором произошла ошибка.",
        description="Путь, в котором произошла ошибка."
    )


class InternalServerErrorResponse(ErrorResponse):
    """
    Сообщение об ошибке 500 Internal Server Error.

    Attributes:

        detail (str): Описание ошибки.
        path (str): Путь, на котором возникла ошибка.
    """
    detail: str = Field(
        "Внутренняя ошибка сервера",
        description="Стандартное сообщение для внутренних ошибок сервера."
    )


class BadRequestResponse(ErrorResponse):
    """
    Сообщение об ошибке 400 Bad Request.

    Attributes:

        detail (str): Описание ошибки.
        path (str): Путь, в котором возникла ошибка.
    """
    detail: str = Field(
        "Ошибка запроса",
        description="Стандартное сообщение для ошибок неверного запроса."
    )


class NotFoundResponse(ErrorResponse):
    """
    Сообщение об ошибке 404 Not Found.

    Attributes:

        detail (str): Описание ошибки.
        path (str): Путь, в котором возникла ошибка.
    """
    detail: str = Field(
        "Ресурс не найден",
        description="Стандартное сообщение для ошибок ненайденных ресурсов."
    )


class UnauthorizedResponse(ErrorResponse):
    """
    Сообщение об ошибке 401 Unauthorized.

    Attributes:

        detail (str): Описание ошибки.
        path (str): Путь, в котором возникла ошибка.
    """
    detail: str = Field(
        "Пользовательская сессия не установлена",
        description="Стандартное сообщение для неавторизованного доступа."
    )