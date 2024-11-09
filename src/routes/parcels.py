"""
Модуль: routes.parcels

Определяет маршруты для обработки HTTP-запросов, связанных с управлением посылками в системе.

Маршруты:

    POST /api/parcels/
        Создать новую посылку.
        Принимает данные в формате JSON и валидирует их.
        Возвращает индивидуальный ULID посылки для идентификации в контексте пользовательской сессии.

    GET /api/parcels/
        Получить список всех посылок, связанных с текущим пользователем.
        Поддерживает пагинацию и фильтрацию по типу посылки и наличию стоимости доставки.

    GET /api/parcels/{parcel_id}/
        Получить детальную информацию о конкретной посылке по её ULID.
        Маршрут не требует проверки сессии и может использоваться получателем посылки.

Зависимости:
    Асинхронная сессия базы данных и идентификатор пользовательской сессии обеспечиваются через FastAPI Dependencies.

"""

import logging
from typing import List
from uuid import UUID

import ulid
from fastapi import APIRouter, Depends, Query, Path, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.parcel import ParcelCreateSchema, ParcelSchema, ParcelReceivedSchema, ParcelResponseSchema
from .dependencies import get_db, get_user_session
from services.parcel_create import ParcelCreateService
from services.parcel import ParcelService
from exceptions.exceptions import ParcelNotFoundError, ParcelDatabaseError, ParcelValidationError
from exceptions.error_schemas import *
logger = logging.getLogger(__name__)
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)


router = APIRouter()



@router.post("/",
             response_model=ParcelReceivedSchema,
             status_code=status.HTTP_201_CREATED,
             responses={
                 status.HTTP_400_BAD_REQUEST: {"model": BadRequestResponse},
                 status.HTTP_401_UNAUTHORIZED: {"model": UnauthorizedResponse},
                 status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": InternalServerErrorResponse},
             },
             summary="Создать новую посылку",
             description="Создание новой посылки. Данные принимаются в формате JSON и валидируются. "
                         "Успешно зарегистрированная посылка возвращает индивидуальный id в формате ULID"
                         "в контексте сессии пользователя.")
async def create_parcel(parcel: ParcelCreateSchema,
                        db: AsyncSession = Depends(get_db),
                        user_session_id: UUID = Depends(get_user_session)):

    try:
        ulid_id = str(ulid.new())

        parcel_data = ParcelSchema(
            id=ulid_id,
            name=parcel.name,
            weight=parcel.weight,
            value=parcel.value,
            parcel_type_id=parcel.parcel_type_id,
            user_session_id=user_session_id,
            shipping_cost= None
        )

        await ParcelCreateService.create_parcel(parcel_data, db)

        return ParcelReceivedSchema(id=ulid_id)

    except ParcelValidationError as e:  # ошибка внутри бизнес-логики, потому 500, а не 422
                                        # пользовательская 422 случится до входа в маршрут, а здесь
                                        # ошибка преобразования внутри нашей логики
        logger.exception(f"Ошибка в данных посылки {parcel.name}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Внутренняя ошибка сервера")

    except ParcelDatabaseError as e:
        logger.exception(f"Ошибка базы данных при создании посылки {parcel.name}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Внутренняя ошибка сервера")

    except Exception as e:
        logger.exception(f"Неизвестная ошибка при создании посылки {parcel.name}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Неизвестная ошибка")

@router.get("/{parcel_id}/",
            response_model=ParcelResponseSchema,
            responses={
                status.HTTP_404_NOT_FOUND: {"model": NotFoundResponse},
                status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": InternalServerErrorResponse},
            },
            summary="Получить данные о посылке по ID",
            description="Возвращает данные по конкретной посылке, включая название, вес, тип и стоимость. "
                        "Сессию не проверяем, может использовать получатель")
async def get_parcel(parcel_id: str = Path(
                    ...,
                    description="Уникальный id посылки в формате ulid, 26 символов",
                    example="01ARZ3NDEKTSV4RRFFQ69G5FAV"),
                    db: AsyncSession = Depends(get_db)):
    try:
        parcel_data = await ParcelService.get_parcel_by_id(parcel_id, db)
        return parcel_data

    except ParcelNotFoundError as e:
        logger.info(str(e))
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    except ParcelValidationError as e:  # ошибка внутри бизнес-логики, потому 500, а не 422
        logger.exception(f"Ошибка в данных посылки {parcel_id}: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Внутренняя ошибка сервера")

    except ParcelDatabaseError as e:
        logger.exception(f"Ошибка базы данных при запросе посылки {parcel_id}: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Внутренняя ошибка сервера")

    except Exception as e:
        logger.exception(f"Неизвестная ошибка при запросе посылки {parcel_id}: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Неизвестная ошибка")


@router.get("/",
            response_model=List[ParcelResponseSchema],
            responses={
                status.HTTP_400_BAD_REQUEST: {"model": BadRequestResponse},
                status.HTTP_401_UNAUTHORIZED: {"model": UnauthorizedResponse},
                status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": InternalServerErrorResponse},
            },
            summary="Получить список своих посылок",
            description="Возвращает список всех посылок текущего пользователя, включая их типы и стоимость доставки. "
                        "Поддерживает пагинацию и фильтрацию по типу и факту наличия стоимости доставки.")
async def get_user_parcels(
        offset: int = 0,
        limit: int = 10,
        parcel_type_id: int | None = Query(None),
        has_shipping_cost: bool | None = Query(None),
        db: AsyncSession = Depends(get_db),
        user_session_id: UUID = Depends(get_user_session)
):
    try:
        parcels = await ParcelService.get_user_parcels(
            db=db,
            user_session_id=user_session_id,
            offset=offset,
            limit=limit,
            parcel_type_id=parcel_type_id,
            has_shipping_cost=has_shipping_cost
        )

        return parcels

    except ParcelValidationError as e:  # ошибка внутри бизнес-логики, потому 500, а не 422
        logger.exception(f"Ошибка в данных посылок для сессии {user_session_id}: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Внутренняя ошибка сервера")

    except ParcelDatabaseError as e:
        logger.exception(f"Ошибка базы данных при запросе посылок для сессии {user_session_id}: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Внутренняя ошибка сервера")

    except Exception as e:
        logger.exception(f"Неизвестная ошибка при запросе посылок для сессии {user_session_id}: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Неизвестная ошибка")