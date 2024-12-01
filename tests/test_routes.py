"""
Модуль: tests/test_routes

Асинхронные тесты для маршрутов parcels
Остальное сделать
+ TODO: Убрать дублирование кода.

"""
import pytest
import pytest_asyncio
from httpx import AsyncClient

# Фикстура для клиента
@pytest_asyncio.fixture
async def client():
    async with AsyncClient(base_url="http://127.0.0.1:8000") as c:
        yield c

# Фикстура для получения куки
@pytest_asyncio.fixture
async def cookies(client):  # Client здесь передается как параметр
    healthy_response = await client.get("/api/healthy")
    assert healthy_response.status_code == 200
    return healthy_response.cookies

# Фикстура для создания посылки
@pytest_asyncio.fixture
async def parcel_id(client, cookies):  # Передаем client и cookies
    payload = {
        "name": "Test Parcel",
        "weight": 5.0,
        "parcel_type_id": 1,
        "value": 100
    }
    client.cookies = cookies  # Устанавливаем куки в клиент
    response = await client.post("/api/parcels/", json=payload)
    assert response.status_code == 201
    return response.json()["id"]

# Тесты
@pytest.mark.asyncio
async def test_get_cookies(cookies):
    """Проверяем, что healthy работает и получена сессия в куки"""
    assert cookies  # Проверяем, что куки получены

@pytest.mark.asyncio
async def test_create_parcel(client, cookies):
    """Проверяем создание посылки"""

    payload = {
        "name": "Test Parcel",
        "weight": 5.0,
        "parcel_type_id": 1,
        "value": 100
    }
    client.cookies = cookies  # Передаем куки в клиент
    response = await client.post("/api/parcels/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert "id" in data

@pytest.mark.asyncio
async def test_get_parcel(client, cookies, parcel_id):
    """Проверяем получение посылки"""
    client.cookies = cookies  # Передаем куки в клиент
    response = await client.get(f"/api/parcels/{parcel_id}/")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == parcel_id
    assert data["name"] == "Test Parcel"
    assert float(data["weight"]) == 5.0
    assert data["parcel_type_id"] == 1
    assert float(data["value"]) == 100
