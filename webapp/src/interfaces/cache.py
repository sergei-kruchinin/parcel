"""
Модуль: interfaces.cache

Назначение:
    Определяет интерфейс для работы с кешированием курса валют.
    Использует `typing.Protocol` для обеспечения гибкости и независимости кода от конкретных реализаций.

Классы:
    ICacheService: Протокол, задающий интерфейс для работы с кэшем курса валют.

Методы:
    get_value(self, key: str) -> str | None:
        Асинхронный метод для получения значения из кэша по ключу.

    set_value(self, key: str, value: str, expire: int | None) -> None:
        Асинхронный метод для записи значения в кэш с указанием времени жизни ключа.
"""

from typing import Protocol


class ICacheService(Protocol):
    """Протокол, задающий интерфейс для работы с кэшем курса валют."""

    async def get_value(self, key: str) -> str | None:
        """
        Получить значение из кэша.

        Args:
            key (str): Ключ, по которому нужно получить значение.

        Returns:
            str | None: Значение из кэша, если оно существует, иначе None.
        """
        ...
    async def set_value(self, key: str, value: str, expire: int | None = None) -> None:
        """
        Сохранить значение в кэш.

        Args:
            key (str): Ключ для сохранения значения.
            value (str): Значение для сохранения.
            expire (int): Время жизни ключа в секундах.
        """
        ...
