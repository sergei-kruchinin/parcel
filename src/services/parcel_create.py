"""
Сервис: services.parcel_create

Сервис для записи посылки непосредственно в БД
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from pydantic import ValidationError
import logging

from models.parcel import ParcelModel
from schemas.parcel import ParcelSchema
from exceptions.exceptions import ParcelDatabaseError, ParcelValidationError

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
        """
        Сохраняет новую посылку в базе данных.

        Args:
            parcel_data (ParcelSchema): Схема посылки, содержащая данные для сохранения.
            db (AsyncSession): Асинхронная сессия для взаимодействия с базой данных.

        Returns:
            ParcelModel: Сохраненная посылка из базы данных (ORM-модель)

        Raises:
            SQLAlchemyError: Если произошла ошибка при работе с базой данных.
        """
        try:
            new_parcel = ParcelModel(**parcel_data.model_dump())
            db.add(new_parcel)
            await db.commit()
            await db.refresh(new_parcel)
            return new_parcel

        except SQLAlchemyError as e:
            await db.rollback()
            logger.exception(f"Ошибка базы данных при создании посылки: {str(e)}")
            raise ParcelDatabaseError(f"Ошибка базы данных при создании посылки: {str(e)}")

        except ValidationError as e:
            logger.exception(f"Ошибка валидации в данных при попытке создания посылки: {str(e)}")
            raise ParcelValidationError(f"Ошибка валидации при попытке создания посылки: {str(e)}")

        except Exception as e:
            logger.exception(f"Неизвестная ошибка при получении посылок для пользователя: {str(e)}")
            raise