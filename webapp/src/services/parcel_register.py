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

class ParcelRegisterService:
    """
    Сервис для записи посылки.
    Запись непосредственно в БД.

    Attributes:
        db (AsyncSession): Асинхронная сессия для взаимодействия с базой данных.
    """


    def __init__(self, db: AsyncSession):
        self.db = db


    async def register_parcel(self,
        parcel_data: ParcelSchema
    ) -> None:
        """
        Сохраняет новую посылку в базе данных.
        Важно: ORM-модель не возвращает, она нам не понадобится.

        Args:
            parcel_data (ParcelSchema): Схема посылки, содержащая данные для сохранения.


        Raises:
            SQLAlchemyError: Если произошла ошибка при работе с базой данных.
        """
        try:
            new_parcel = ParcelModel(**parcel_data.model_dump())
            self.db.add(new_parcel)
            await self.db.commit()
            await self.db.refresh(new_parcel)

        except SQLAlchemyError as e:
            await self.db.rollback()
            logger.exception(f"Ошибка базы данных при создании посылки: {str(e)}")
            raise ParcelDatabaseError(f"Ошибка базы данных при создании посылки: {str(e)}")

        except ValidationError as e:
            logger.exception(f"Ошибка валидации в данных при попытке создания посылки: {str(e)}")
            raise ParcelValidationError(f"Ошибка валидации при попытке создания посылки: {str(e)}")

        except Exception as e:
            logger.exception(f"Неизвестная ошибка при получении посылок для пользователя: {str(e)}")
            raise