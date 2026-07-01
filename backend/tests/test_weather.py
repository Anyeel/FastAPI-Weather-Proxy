from datetime import datetime, timezone, timedelta
from unittest.mock import MagicMock, AsyncMock

from fastapi.testclient import TestClient

from backend.core.http_client import get_client
from backend.database.session import get_db
from backend.main import app
from backend.models.weather import City, WeatherInformation


def test_get_weather_city_not_found():
    """Tests the /weather/ endpoint for a city ID that does not exist in the local database."""

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
        response = client.get("/weather/99")

    app.dependency_overrides.clear()

    assert response.status_code == 404


def test_get_multiple_weather_success():
    """Tests the /weather/ endpoint for multiple city IDs, ensuring response is formatted correctly."""

    # Mock for db
    mock_db_session = AsyncMock()
    mock_db_session.add = MagicMock()
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = None
    mock_db_session.execute.return_value = mock_result

    # Mock for OpenWeather
    mock_http_client = AsyncMock()
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "id": 1,
        "name": "Granada",
        "coord": {"lat": 37.1, "lon": -3.6},
        "main": {"temp": 22.5, "humidity": 40},
        "weather": [{"description": "sunny"}]
    }
    mock_http_client.get.return_value = mock_response

    # These functions replace real dependencies (Database and Internet) with our mocks to isolate the test.
    async def override_get_db():
        yield mock_db_session

    async def override_get_client():
        yield mock_http_client

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_client] = override_get_client

    with TestClient(app) as client:
        response = client.get("/weather/?cities=1")

    app.dependency_overrides.clear()

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["city_id"] == 1
    assert data[0]["city_name"] == "Granada"
    assert data[0]["temperature"] == 22.5
    assert data[0]["description"] == "sunny"
    assert data[0]["humidity"] == 40


def test_weather_cache_expired():
    """Tests that the /weather/ endpoint fetches fresh data when the cached data is older than the TTL."""

    mock_city = City(id=1, name="Amsterdam", lat=52.37, lon=4.88)

    # Old data
    old_time = datetime.now(timezone.utc) - timedelta(hours=5)
    mock_weather = WeatherInformation(
        city_id=1,
        temperature=10.0,
        description="cold",
        humidity=80,
        updated_at=old_time
    )

    mock_db_session = AsyncMock()
    mock_db_session.add = MagicMock()
    mock_result = MagicMock()

    # Responses in order
    mock_result.scalar_one_or_none.side_effect = [mock_city, mock_weather]
    mock_db_session.execute.return_value = mock_result

    mock_http_client = AsyncMock()
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "id": 1,
        "name": "Granada",
        "coord": {"lat": 37.1, "lon": -3.6},
        "main": {"temp": 25.0, "humidity": 40},  # New data
        "weather": [{"description": "sunny"}]
    }
    mock_http_client.get.return_value = mock_response

    async def override_get_db():
        yield mock_db_session

    async def override_get_client():
        yield mock_http_client

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_client] = override_get_client

    with TestClient(app) as client:
        response = client.get("/weather/?cities=1")

    app.dependency_overrides.clear()

    assert response.status_code == 200
    data = response.json()

    assert data[0]["temperature"] == 25.0

    # If cache is used an error will occur
    mock_http_client.get.assert_called_once()
