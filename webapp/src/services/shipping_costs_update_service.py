"""
Модуль services.pricing_update_currency
Служит для обновления курса доллара
"""
import logging
from decimal import Decimal, InvalidOperation

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError

from models.parcel import ParcelModel  # Предполагается, что модель ParcelModel импортируется здесь

logger = logging.getLogger(__name__)


class ShippingCostsUpdateService:
    """
    Сервис для обновления стоимости доставки в зависимости от курса валют.

    Attributes:
        db (AsyncSession): Асинхронная сессия для взаимодействия с базой данных.
    """

    def __init__(self, db: AsyncSession):
        self.db = db

    async def update_shipping_costs(self, usd_to_rub: Decimal):
        """
        Обновляет стоимость доставки для всех посылок с неопределенной стоимостью.

        Args:
            usd_to_rub (Decimal): Курс доллара к рублю.
        """
        try:
            # Получаем все посылки без расчетной стоимости
            result = await self.db.execute(
                select(ParcelModel).filter(ParcelModel.shipping_cost.is_(None))
            )
            parcels = result.scalars().all()

            # Обновляем стоимость доставки для каждой посылки
            for parcel in parcels:
                try:
                    weight = Decimal(parcel.weight)
                    value = Decimal(parcel.value)
                    new_shipping_cost = (weight * Decimal('0.5') + value * Decimal('0.01')) * usd_to_rub
                    parcel.shipping_cost = new_shipping_cost
                    logger.debug(f"Обновлена стоимость доставки для посылки {parcel.id}: {new_shipping_cost}")
                except (ValueError, InvalidOperation) as e:
                    logger.warning(f"Ошибка при расчете стоимости для посылки {parcel.id}: {e}")

            # Сохраняем изменения
            await self.db.commit()
            logger.info("Стоимость доставки успешно обновлена для всех посылок без расчетной стоимости.")
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при работе с БД: {e}")
            await self.db.rollback()
            raise
        except Exception as e:
            logger.error(f"Общая ошибка при обновлении стоимости доставки: {e}")
            await self.db.rollback()
            raise
