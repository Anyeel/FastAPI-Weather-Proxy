from datetime import timedelta

import httpx
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.config import settings
from backend.core.http_client import get_client
from backend.models.weather import City, WeatherInformation
from backend.schemas.weather import WeatherResponse
from backend.services.base import BaseWeatherService
from backend.utils.cache import is_cache_valid
from backend.utils.exceptions import handle_api_errors


class WeatherService(BaseWeatherService):
    """Service class to handle weather-related business logic and external API calls."""

    CACHE_TTL = timedelta(hours=3)

    def __init__(self, client: httpx.AsyncClient = Depends(get_client)):
        """Initializes the WeatherService with an injected HTTP client.

        Args:
            client (httpx.AsyncClient): Injected HTTP client to execute external API calls safely.
        """
        super().__init__(client)

    def _build_response(self, city: City, temperature: float, description: str, humidity: int) -> WeatherResponse:
        """Helper method to centralize the creation of the Pydantic response model."""
        return WeatherResponse(
            city_id=city.id,
            city_name=city.name,
            temperature=temperature,
            description=description,
            humidity=humidity
        )

    @handle_api_errors
    async def fetch_weather_by_id(self, city_id: int, db: AsyncSession) -> WeatherResponse:
        """Fetches current weather data for a specific city by its ID.

        Makes an asynchronous HTTP request to the OpenWeatherMap API using the
        injected HTTP client. Uses metric units to return temperature in Celsius.

        Args:
            city_id (int): The unique OpenWeatherMap city ID.
            db (AsyncSession): The database session to query and update the cache.

        Returns:
            WeatherResponse: A validated Pydantic model containing the weather data.

        Raises:
            HTTPException: If the city ID is not found in OpenWeatherMap (404).
        """

        # Search the city in our DB
        stmt = select(City).where(City.id == city_id)
        city = (await db.execute(stmt)).scalar_one_or_none()

        url = f"{settings.openweathermap_base_url}/weather"

        # Case City is not in our DB
        if not city:
            params = settings.base_weather_params | {"id": city_id}

            data = await self._fetch_from_api(url, params)

            new_city = City(
                id=city_id,
                name=data["name"],
                lat=data["coord"]["lat"],
                lon=data["coord"]["lon"]
            )
            db.add(new_city)

            temp = data["main"]["temp"]
            desc = data["weather"][0]["description"]
            hum = data["main"]["humidity"]

            new_weather = WeatherInformation(
                city_id=city_id, temperature=temp, description=desc, humidity=hum
            )
            db.add(new_weather)

            await db.commit()

            return self._build_response(new_city, temp, desc, hum)

        # Case City is in our DB
        cache_stmt = select(WeatherInformation).where(WeatherInformation.city_id == city_id)
        weather_cache = (await db.execute(cache_stmt)).scalar_one_or_none()

        if weather_cache and is_cache_valid(weather_cache.updated_at, ttl=self.CACHE_TTL):
            return self._build_response(
                city, weather_cache.temperature, weather_cache.description, weather_cache.humidity
            )

        params = settings.base_weather_params | {"lat": city.lat, "lon": city.lon}

        data = await self._fetch_from_api(url, params)

        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"]
        hum = data["main"]["humidity"]

        if weather_cache:
            weather_cache.temperature = temp
            weather_cache.description = desc
            weather_cache.humidity = hum
        else:
            weather_cache = WeatherInformation(
                city_id=city.id, temperature=temp, description=desc, humidity=hum
            )
            db.add(weather_cache)

        await db.commit()

        return self._build_response(city, temp, desc, hum)

    async def fetch_multiple_weather(self, city_ids: list[int], db: AsyncSession) -> list[WeatherResponse]:
        """Fetches current weather data for multiple cities concurrently.

        Args:
            city_ids (list[int]): A list of unique OpenWeatherMap city IDs.
            db (AsyncSession): The database session passed from the router.
        Returns:
            list[WeatherResponse]: A list of validated weather data objects.
        """

        results = []
        for city_id in city_ids:
            weather = await self.fetch_weather_by_id(city_id, db)
            results.append(weather)

        return results

    @handle_api_errors
    async def search_cities(self, query: str) -> list[dict]:
        """Searches for cities matching a query string using the external API.

        Args:
            query (str): The city name or partial name to search for.

        Returns:
            list[dict]: A list of dictionaries containing city id, name, and country.

        Raises:
            HTTPException: If the external API request fails or returns an error.
        """
        url = f"{settings.openweathermap_base_url}/find"

        # cnt limits the results to the top 5 matches
        params = settings.base_weather_params | {"q": query, "type": "like", "cnt": 5}

        data = await self._fetch_from_api(url, params)

        results = []
        for item in data.get("list", []):
            results.append({
                "id": item["id"],
                "name": item["name"],
                "country": item["sys"]["country"]
            })

        return results
