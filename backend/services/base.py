import httpx
from fastapi import HTTPException


class BaseWeatherService:
    """Base class containing shared logic for weather-related services."""

    def __init__(self, client: httpx.AsyncClient):
        """
        Initializes the service with an injected HTTP client.

        Args:
            client (httpx.AsyncClient): The asynchronous HTTP client for API requests.
        """
        self.client = client

    async def _fetch_from_api(self, url: str, params: dict, city_id: int = None) -> dict:
        """
        Executes an HTTP GET request to OpenWeatherMap and returns the parsed JSON data.

        Args:
            url (str): The target API endpoint.
            params (dict): Query parameters including API key and city identifiers.
            city_id (int, optional): The OpenWeather city ID for specific error messaging.

        Returns:
            dict: The validated JSON response from the API.

        Raises:
            HTTPException: If the city is not found (404) or the API returns an error.
        """
        response = await self.client.get(url, params=params)

        # ID not in OpenWeather
        if response.status_code == 404:
            msg = f"City ID {city_id} not found" if city_id else "City not found"
            raise HTTPException(status_code=404, detail=f"{msg} in OpenWeatherMap.")

        response.raise_for_status()
        return response.json()
