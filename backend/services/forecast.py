import httpx
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.config import settings
from backend.core.http_client import get_client
from backend.models.weather import City
from backend.schemas.forecast import CityForecastResponse, ForecastItem
from backend.services.base import BaseWeatherService
from backend.utils.exceptions import handle_api_errors


class ForecastService(BaseWeatherService):
    """Service class to handle forecast-related business logic and external API calls."""

    def __init__(self, client: httpx.AsyncClient = Depends(get_client)):
        """Initializes the ForecastService with an injected HTTP client.

        Args:
            client (httpx.AsyncClient): Injected HTTP client to execute external API calls safely.
        """
        super().__init__(client)

    @handle_api_errors
    async def fetch_forecast_by_id(self, city_id: int, db: AsyncSession) -> CityForecastResponse:
        """Fetches the 5-day forecast data for a specific city by its ID.

        Makes an asynchronous HTTP request to the OpenWeatherMap API using the
        injected HTTP client.

        Args:
            city_id (int): The unique OpenWeatherMap city ID.
            db (AsyncSession): The database session to query and update the cache.

        Returns:
            CityForecastResponse: A validated model containing the city's forecast.

        Raises:
            HTTPException: If the city ID is not found in OpenWeatherMap (404).
        """

        stmt = select(City).where(City.id == city_id)
        city = (await db.execute(stmt)).scalar_one_or_none()

        url = f"{settings.openweathermap_base_url}/forecast"

        if not city:
            params = settings.base_weather_params | {"id": city_id}
        else:
            params = settings.base_weather_params | {"lat": city.lat, "lon": city.lon}

        data = await self._fetch_from_api(url, params, city_id=city_id)

        if not city:
            city_data = data["city"]
            new_city = City(
                id=city_id,
                name=city_data["name"],
                lat=city_data["coord"]["lat"],
                lon=city_data["coord"]["lon"]
            )
            db.add(new_city)
            await db.commit()

            city_name = city_data["name"]
        else:
            city_name = city.name

        forecast_items = [
            ForecastItem(
                timestamp=item["dt_txt"],
                temperature=item["main"]["temp"],
                description=item["weather"][0]["description"]
            )
            for item in data.get("list", [])
        ]

        return CityForecastResponse(
            city_id=city_id,
            city_name=city_name,
            forecasts=forecast_items
        )

    async def fetch_multiple_forecasts(self, city_ids: list[int], db: AsyncSession) -> list[CityForecastResponse]:
        """Fetches 5-day forecast data for multiple cities concurrently.

        Args:
            city_ids (list[int]): A list of unique OpenWeatherMap city IDs.
            db (AsyncSession): The database session passed from the router.

        Returns:
            list[CityForecastResponse]: A list of validated forecast data objects.
        """
        results = []
        for city_id in city_ids:
            forecast = await self.fetch_forecast_by_id(city_id, db)
            results.append(forecast)

        return results
