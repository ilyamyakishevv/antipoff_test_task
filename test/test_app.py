import pytest
from httpx import AsyncClient
from app import app

@pytest.mark.asyncio
async def test_query_endpoint():
    request_payload = {
        "cadastre_number": "12345",
        "latitude": "40.7128",
        "longitude": "74.0060"
    }
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/query", json=request_payload)
        assert response.status_code == 200
        assert "message" in response.json()

@pytest.mark.asyncio
async def test_result_endpoint():
    response_payload = {
        "id": 1,
        "result": True
    }
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/result", json=response_payload)
        assert response.status_code == 200
        assert "message" in response.json()

@pytest.mark.asyncio
async def test_total_history_endpoint():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/total_history")
        assert response.status_code == 200
        assert "all requests" in response.json()

@pytest.mark.asyncio
async def test_get_history_endpoint():
    cadastre_number = "12345"
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get(f"/history/{cadastre_number}")
        assert response.status_code == 200
        assert f"history for query by cadastre number {cadastre_number}" in response.json()
