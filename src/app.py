"""
Модуль: app

Используется в Dockerfile для создания и запуска Docker контейнера.

"""

from fastapi import FastAPI

from routes import parcels

app = FastAPI()

app.include_router(parcels.router, prefix="/api/parcels")
