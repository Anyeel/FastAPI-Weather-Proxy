from pydantic import BaseModel


class ForecastItem(BaseModel):
    """Single forecast data point (typically at 3-hour intervals).

    Attributes:
        timestamp (str): Date and time of the forecast in text format (e.g., "2024-03-15 12:00:00").
        temperature (float): Expected temperature in Celsius.
        description (str): Weather condition description.
    """
    timestamp: str
    temperature: float
    description: str


class CityForecastResponse(BaseModel):
    """5-day forecast response model for a specific city.

    Attributes:
        city_id (int): Unique identifier of the city.
        city_name (str): Name of the city.
        forecasts (list[ForecastItem]): List of forecasted weather conditions.
    """
    city_id: int
    city_name: str
    forecasts: list[ForecastItem]
