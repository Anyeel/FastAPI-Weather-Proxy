from typing import Any

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Class for handle environment variables.

    Attributes:
        openweathermap_base_url (str): Base URL for the OpenWeatherMap API.
        openweathermap_api_key (str): Access key for the API.
        database_url (str): Connection string for the PostgreSQL database.
    """
    openweathermap_base_url: str = "https://api.openweathermap.org/data/2.5"
    openweathermap_api_key: str

    # Default params
    weather_units: str = "metric"
    weather_lang: str = "en"

    database_url: str

    # Ignore allows additional environment variables in .env without raising validation errors.
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @property
    def base_weather_params(self) -> dict[str, Any]:
        """Returns the default parameters needed for all OpenWeather requests."""
        return {
            "appid": self.openweathermap_api_key,
            "units": self.weather_units,
            "lang": self.weather_lang
        }

    BACKEND_CORS_ORIGINS: list[str] = [
        "http://localhost:4200",
        "http://127.0.0.1:4200"
    ]


settings = Settings()
