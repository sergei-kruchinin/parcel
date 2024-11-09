"""
Сервис: services.parcel_create

Сервис для записи посылки непосредственно в БД
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
import logging

from models.parcel import ParcelModel
from schemas.parcel import ParcelSchema

logger = logging.getLogger(__name__)
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

class ParcelCreateService:
    """
    Сервис для записи посылки.
    Запись непосредственно в БД
    """


    @staticmethod
    async def create_parcel(
        parcel_data: ParcelSchema,
        db: AsyncSession
    ) -> ParcelModel:
        """Сохраняет новую посылку в базе данных."""
        try:
            new_parcel = ParcelModel(**parcel_data.model_dump())
            db.add(new_parcel)
            await db.commit()
            await db.refresh(new_parcel)
            return new_parcel

        except SQLAlchemyError as e:
            await db.rollback()
            logger.error(f"Ошибка при создании посылки: {e}")
            raise e