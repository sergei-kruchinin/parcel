"""
Сервис: services.parcel

Служит для получения информации о посылках из БД

"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from models.parcel import ParcelModel
from schemas.parcel import ParcelResponseSchema

class ParcelService:
    """Сервис для получения информации о посылках из БД"""

    @staticmethod
    async def get_parcel_by_id(parcel_id: str, db: AsyncSession) -> ParcelResponseSchema:
        """Получает данные о посылке по её ID."""
        # Выполнение запроса к базе данных
        result = await db.execute(
            select(ParcelModel)
            .options(selectinload(ParcelModel.parcel_type))
            .where(ParcelModel.id == parcel_id)  # type: ignore
        )
        parcel = result.scalars().first()

        if not parcel:
            raise ValueError("Посылка с таким ID не найдена.")

        # Формирование ответа. Важно: пользовательскую сессию не включаем
        response = ParcelResponseSchema(
            id=parcel.id,
            name=parcel.name,
            weight=parcel.weight,
            parcel_type_id=parcel.parcel_type_id,
            parcel_type_name=parcel.parcel_type.name,
            value=parcel.value,
            shipping_cost=parcel.shipping_cost
        )

        return response