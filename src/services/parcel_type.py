"""
Сервис: services.parcel_type

Служит для получения информации о типах посылок из БД

"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from pydantic import ValidationError
from typing import List
import logging

from models.parcel import ParcelTypeModel
from schemas.parcel_type import ParcelTypeResponseSchema
from exceptions.exceptions import ParcelDatabaseError, ParcelValidationError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ParcelTypeService:
    """Сервис для получения информации о посылках из БД"""

    @staticmethod
    async def get_parcel_types(db: AsyncSession) -> List[ParcelTypeResponseSchema]:
        """
        Получает список типов посылок из базы данных.

        Args:
            db (AsyncSession): Асинхронная сессия базы данных.

        Returns:
            List[ParcelTypeResponseSchema]: Список типов посылок

        Raises:
            ParcelValidationError: Ошибка валидации
            ParcelDatabaseError: Ошибка базы данных
            Exception: Неизвестная ошибка при получении посылок для пользователя
            """
        try:
            result = await db.execute(select(ParcelTypeModel).order_by(ParcelTypeModel.id))
            parcel_types = result.scalars().all()
            response_list = [
                ParcelTypeResponseSchema(
                    id=parcel_type.id,
                    name=parcel_type.name)
                for parcel_type in parcel_types ]

            return response_list


        except ValidationError as e:
            logger.exception(f"Ошибка валидации данных типа посылки: {str(e)}")
            raise ParcelValidationError(f"Ошибка валидации данных типа посылки: {str(e)}")

        except SQLAlchemyError as e:
            logger.exception(f"Ошибка базы данных при получении данных типа посылки: {str(e)}")
            raise ParcelDatabaseError(f"Ошибка базы данных: {str(e)}")

        except Exception as e:
            logger.exception(f"Неизвестная ошибка при получении данных типа посылки: {str(e)}")
            raise