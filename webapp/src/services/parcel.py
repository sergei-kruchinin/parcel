"""
Модуль: services.parcel

Служит для получения информации о посылках из базы данных, используя SQLAlchemy.
Предоставляет методы для получения данных о конкретной посылке и списка посылок для пользователя,
с поддержкой фильтрации и пагинации.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import SQLAlchemyError
from pydantic import ValidationError
from uuid import UUID
from typing import List
import logging

from models.parcel import ParcelModel
from schemas.parcel import ParcelResponseSchema
from exceptions.exceptions import ParcelNotFoundError, ParcelDatabaseError, ParcelValidationError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Глобальная переменная для значения, используемого, когда стоимость доставки не рассчитана.
# Можно было бы сделать через pydantic, но мы сделаем просто попроще.
SHIPPING_COST_NOT_CALCULATED = "Не рассчитано"


class ParcelService:
    """
    Сервис для получения информации о посылках из базы данных.

    Использует SQLAlchemy для выполнения асинхронных запросов к базе данных. Предоставляет методы для
    получения данных о конкретной посылке и списка посылок для конкретного пользователя.

    Attributes:
        db (AsyncSession): Асинхронная сессия для взаимодействия с базой данных.
    """


    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_parcel_by_id(self, parcel_id: str) -> ParcelResponseSchema:
        """
        Получает данные о посылке по её ID.

        Args:
            parcel_id (str): Уникальный ID посылки для получения (ulid).

        Returns:
            ParcelResponseSchema: Схема с детальной информацией о посылке.

        Raises:
            ParcelNotFoundError: Посылка не найдена
            ParcelValidationError: Ошибка валидации данных
            ParcelDatabaseError: Ошибка базы данных
            Exception: Неизвестная ошибка при получении посылки
        """
        try:
            logger.info(f"Поиск информации о посылке {parcel_id}")

            result = await self.db.execute(
                select(ParcelModel)
                .options(selectinload(ParcelModel.parcel_type))
                .where(ParcelModel.id == parcel_id)  # type: ignore
            )
            parcel = result.scalars().first()

            if not parcel:
                logger.warning(f"Посылка с ID {parcel_id} не найдена.")
                raise ParcelNotFoundError(f"Посылка с ID {parcel_id} не найдена.")

            # Формирование ответа. Важно: пользовательскую сессию не включаем (из соображений безопасности)
            response = ParcelResponseSchema(
                id=parcel.id,
                name=parcel.name,
                weight=parcel.weight,
                parcel_type_id=parcel.parcel_type_id,
                parcel_type_name=parcel.parcel_type.name,
                value=parcel.value,
                shipping_cost=parcel.shipping_cost or SHIPPING_COST_NOT_CALCULATED
            )

            logger.info(f"Посылка с ID {parcel_id} успешно найдена.")
            return response


        except ParcelNotFoundError as e:
            raise e

        except ValidationError as e:
            logger.exception(f"Ошибка валидации данных для посылки с ID {parcel_id}: {str(e)}")
            raise ParcelValidationError(f"Ошибка валидации данных: {str(e)}")

        except SQLAlchemyError as e:
            logger.exception(f"Ошибка базы данных при получении посылки с ID {parcel_id}: {str(e)}")
            raise ParcelDatabaseError(f"Ошибка базы данных: {str(e)}")

        except Exception as e:
            logger.exception(f"Неизвестная ошибка при получении посылки с ID {parcel_id}: {str(e)}")
            raise e


    async def get_user_parcels(
            self,
            user_session_id: UUID,
            offset: int = 0,
            limit: int = 30,
            parcel_type_id: int | None = None,
            has_shipping_cost: bool | None  = None
    ) -> List[ParcelResponseSchema]:
        """
        Получает список посылок текущего пользователя с возможностью фильтрации.

        Args:
            user_session_id (UUID): Идентификатор пользовательской сессии для фильтрации посылок,
            offset (int): Смещение для пагинации, по умолчанию 0,
            limit (int): Максимальное количество посылок для получения, по умолчанию 30,
            parcel_type_id (int|None): Необязательный параметр для возможности фильтровать посылки по ID типа посылки,
            has_shipping_cost (bool|None): Необязательный параметр для возможности фильтровать посылки
                по факту наличия рассчитанной стоимости доставки.

        Returns:
            List[ParcelResponseSchema]: Список объектов ParcelResponseSchema с информацией о посылках.

        Raises:
            ParcelValidationError: Ошибка валидации
            ParcelDatabaseError: Ошибка базы данных
            Exception: Неизвестная ошибка при получении посылок для пользователя
        """
        try:
            logger.info(f"Поиск информации о посылках для пользователя с сессией {user_session_id}.")
            query = select(ParcelModel).options(selectinload(ParcelModel.parcel_type)).where(
                ParcelModel.user_session_id == user_session_id  # type: ignore
            )

            # если задана фильтрация по типу посылки...
            if parcel_type_id is not None:
                query = query.where(ParcelModel.parcel_type_id == parcel_type_id)

            # если задана фильтрация по факту наличия рассчитанной стоимости доставки...
            if has_shipping_cost is not None:
                if has_shipping_cost:
                    query = query.where(ParcelModel.shipping_cost.isnot(None))
                else:
                    query = query.where(ParcelModel.shipping_cost.is_(None))

            # Так как используем ULID, добавляем сортировку по полю id
            query = query.order_by(ParcelModel.id)

            result = await self.db.execute(query.offset(offset).limit(limit))
            parcels = result.scalars().all()
            response_list = [
                ParcelResponseSchema(
                    id=parcel.id,
                    name=parcel.name,
                    weight=parcel.weight,
                    parcel_type_id=parcel.parcel_type_id,
                    parcel_type_name=parcel.parcel_type.name,
                    value=parcel.value,
                    shipping_cost = parcel.shipping_cost or SHIPPING_COST_NOT_CALCULATED
                )
                for parcel in parcels
            ]

            logger.info(f"Получено {len(response_list)} посылок для пользователя с сессией {user_session_id}.")
            return response_list

        except ValidationError as e:
            logger.exception(f"Ошибка валидации при получении посылок для пользователя {user_session_id}: {str(e)}")
            raise ParcelValidationError(f"Ошибка валидации: {str(e)}")

        except SQLAlchemyError as e:
            logger.exception(f"Ошибка базы данных при получении посылок для пользователя {user_session_id}: {str(e)}")
            raise ParcelDatabaseError(f"Ошибка базы данных: {str(e)}")

        except Exception as e:
            logger.exception(f"Неизвестная ошибка при получении посылок для пользователя {user_session_id}: {str(e)}")
            raise