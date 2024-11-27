# Модуль: internal_service_app

import logging
from fastapi import FastAPI
from routes.internal_services import router, lifespan
from routes import healthy

# Настраиваем логгирование приложения
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Создаем экземпляр FastAPI, передавая lifespan для инициализации и завершения Redis пула
app = FastAPI(lifespan=lifespan)

# Подключаем роуты из модуля internal_services
app.include_router(router, prefix='/api')
app.include_router(healthy.router, prefix="/api/healthy")


