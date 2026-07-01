from typing import Annotated

from fastapi import APIRouter, Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database.session import get_db
from backend.schemas.forecast import CityForecastResponse
from backend.services.forecast import ForecastService
from backend.utils.validators import parse_comma_separated_cities

router = APIRouter(
    prefix="/forecast",
    tags=["Forecast"]
)

db_dependency = Annotated[AsyncSession, Depends(get_db)]


@router.get("/", response_model=list[CityForecastResponse])
async def get_multiple_forecasts(
        db: db_dependency,
        cities: str = Query(..., description="Comma separated city IDs (e.g., 3117735,2517117,2759794)"),
        forecast_service: ForecastService = Depends()
):
    """Retrieves the 5-day weather forecast for multiple cities simultaneously.

    Args:
        cities (str): A comma-separated string of city IDs provided as a query parameter.
        db (AsyncSession): Injected database session for city persistence and lookup.
        forecast_service (ForecastService): Injected service handling business logic and API calls.

    Returns:
        list[CityForecastResponse]: A list containing the forecast data for each city.

    Raises:
        HTTPException: If the provided city IDs cannot be parsed into integers.
    """
    city_id_list = parse_comma_separated_cities(cities)

    return await forecast_service.fetch_multiple_forecasts(city_id_list, db)
