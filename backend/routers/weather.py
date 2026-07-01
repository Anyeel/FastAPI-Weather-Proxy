from typing import Annotated

from fastapi import APIRouter, Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database.session import get_db
from backend.schemas.weather import WeatherResponse, CitySearchResponse
from backend.services.weather import WeatherService
from backend.utils.validators import parse_comma_separated_cities

router = APIRouter(
    prefix="/weather",
    tags=["Weather"]
)

db_dependency = Annotated[AsyncSession, Depends(get_db)]


@router.get("/search", response_model=list[CitySearchResponse])
async def search_cities(
        q: str = Query(..., min_length=2, description="City name to search for"),
        service: WeatherService = Depends(WeatherService)
):
    """Retrieves a list of cities matching the provided search query.

    Args:
        q (str): The city name query string provided as a query parameter.
        service (WeatherService): Injected service handling business logic and API calls.

    Returns:
        list[CitySearchResponse]: A list containing the matching cities and their IDs.

    Raises:
        HTTPException: If the search query is invalid or the external API fails.
    """
    return await service.search_cities(query=q)


@router.get("/{city_id}", response_model=WeatherResponse)
async def get_weather(
        city_id: int,
        db: db_dependency,
        weather_service: WeatherService = Depends()
):
    """Retrieves the current weather for a single city.

    Args:
        city_id (int): The OpenWeatherMap city ID provided in the URL path.
        db (AsyncSession): The injected database session for cache operations.
        weather_service (WeatherService): Injected service handling business logic and API calls.

    Returns:
        WeatherResponse: The current weather data for the requested city.
    """
    return await weather_service.fetch_weather_by_id(city_id, db)


@router.get("/", response_model=list[WeatherResponse])
async def get_multiple_weather(
        db: db_dependency,
        cities: str = Query(..., description="Comma separated city IDs (e.g., 3117735,2517117,2759794)"),
        weather_service: WeatherService = Depends()
):
    """Retrieves the current weather for multiple cities simultaneously.

    Args:
        cities (str): A comma-separated string of city IDs provided as a query parameter.
        db (AsyncSession): The injected database session for cache operations.
        weather_service (WeatherService): Injected service handling business logic and API calls.

    Returns:
        list[WeatherResponse]: A list containing the weather data for each city.

    Raises:
        HTTPException: If the provided city IDs cannot be parsed into integers.
    """
    city_id_list = parse_comma_separated_cities(cities)

    return await weather_service.fetch_multiple_weather(city_id_list, db)
