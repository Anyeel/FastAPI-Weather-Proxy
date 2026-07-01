from unittest.mock import MagicMock, AsyncMock

from fastapi.testclient import TestClient

from backend.core.http_client import get_client
from backend.database.session import get_db
from backend.main import app
from backend.models.weather import City


def test_get_forecast_city_not_found():
    """Tests the /forecast/ endpoint for a city ID that does not exist in the local database."""

    # Mock for db
    mock_db_session = AsyncMock()
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = None
    mock_db_session.execute.return_value = mock_result

    # Mock for OpenWeather
    mock_http_client = AsyncMock()
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_response.raise_for_status.side_effect = Exception("404 Not Found")
    mock_http_client.get.return_value = mock_response

    # Mock dependency providers
    async def override_get_db():
        yield mock_db_session

    async def override_get_client():
        yield mock_http_client

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_client] = override_get_client

    with TestClient(app) as client:
        response = client.get("/forecast/?cities=99")

    app.dependency_overrides.clear()

    assert response.status_code == 404


def test_get_multiple_forecasts_success():
    """Tests the /forecast/ endpoint for multiple city IDs, ensuring that the response is correctly formatted and contains the expected data."""

    # Mock for db (City exists in cache)
    mock_db_session = AsyncMock()
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = City(id=1, name="Granada")
    mock_db_session.execute.return_value = mock_result

    # Mock for OpenWeather (Forecast JSON format)
    mock_http_client = AsyncMock()
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "list": [
            {
                "dt_txt": "2026-03-15 12:00:00",
                "main": {"temp": 18.5, "humidity": 40},
                "weather": [{"description": "scattered clouds"}]
            },
            {
                "dt_txt": "2026-03-15 15:00:00",
                "main": {"temp": 20.0, "humidity": 45},
                "weather": [{"description": "light rain"}]
            }
        ],
        "city": {
            "id": 1,
            "name": "Granada",
            "coord": {"lat": 37.1, "lon": -3.6}
        }
    }
    mock_http_client.get.return_value = mock_response

    # Mock dependency providers
    async def override_get_db():
        yield mock_db_session

    async def override_get_client():
        yield mock_http_client

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_client] = override_get_client

    with TestClient(app) as client:
        response = client.get("/forecast/?cities=1")

    app.dependency_overrides.clear()

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["city_id"] == 1
    assert data[0]["city_name"] == "Granada"

    forecasts = data[0]["forecasts"]
    assert len(forecasts) == 2

    assert forecasts[0]["temperature"] == 18.5
    assert forecasts[0]["description"] == "scattered clouds"

    assert forecasts[1]["temperature"] == 20.0
    assert forecasts[1]["description"] == "light rain"
