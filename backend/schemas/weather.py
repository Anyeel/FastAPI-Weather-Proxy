from pydantic import BaseModel


class WeatherResponse(BaseModel):
    """Response model for a city's weather.

    Attributes:
        city_id (int): Unique identifier of the city.
        city_name (str): Name of the city.
        temperature (float): Current temperature in Celsius degrees.
        description (str): Weather condition description.
        humidity (int): Humidity percentage.
    """
    city_id: int
    city_name: str
    temperature: float
    description: str
    humidity: int


class CitySearchResponse(BaseModel):
    """Response model for a city search result.

    Attributes:
        id (int): Unique OpenWeatherMap identifier of the city.
        name (str): Name of the matching city.
        country (str): Two-letter country code of the city.
    """
    id: int
    name: str
    country: str
