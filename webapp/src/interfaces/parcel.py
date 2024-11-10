"""
Модуль: interfaces.parcel

Содержит интерфейсы для службы управления посылками.
Интерфейсы определены с помощью модуля `typing.Protocol`, чтобы обеспечить независимость кода от конкретных реализаций.

Классы:
    IParcelRegisterService: Протокол, задающий интерфейс для службы регистрации посылок.

Интерфейсы:
    register_parcel(parcel_data: ParcelSchema) -> None: Асинхронный метод, предназначенный для регистрации новой посылки
"""

from typing import Protocol
from schemas.parcel import ParcelSchema

class IParcelRegisterService(Protocol):
    """Протокол, задающий интерфейс для службы регистрации посылок."""

    async def register_parcel(self, parcel_data: ParcelSchema) -> None:
        """
        Зарегистрировать новую посылку.

        Args:
            parcel_data (ParcelSchema): Данные для регистрации новой посылки.

        Returns:
            None
        """
        ...