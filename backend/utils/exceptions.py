import functools
from typing import Callable, Any

import httpx
from fastapi import HTTPException


def handle_api_errors(func: Callable) -> Callable:
    """Decorator to handle HTTP errors when consuming external APIs.

    Catches httpx exceptions and converts them into FastAPI HTTPExceptions
    to return appropriate responses to the client.

    Args:
        func (Callable): Asynchronous function to decorate.

    Returns:
        Callable: Wrapped function with error handling.

    Raises:
        HTTPException: If a network error occurs or the external API fails.
    """

    @functools.wraps(func)
    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return await func(*args, **kwargs)

        except httpx.HTTPStatusError as e:
            status_code = e.response.status_code

            try:
                error_data = e.response.json()
                error_msg = error_data.get("message", "Unknown error")
            except ValueError:
                error_msg = "Unknown external API error"

            if status_code == 404:
                raise HTTPException(status_code=404, detail=f"City not found: {error_msg}")
            elif status_code == 401:
                raise HTTPException(status_code=401, detail=f"Unauthorized: Check OpenWeather API Key. ({error_msg})")
            elif status_code == 400:
                raise HTTPException(status_code=400, detail=f"Bad request to external API: {error_msg}")

            # Fallback for other 4xx or 5xx errors from OpenWeatherMap
            raise HTTPException(status_code=status_code, detail=f"External API error: {error_msg}")

        except httpx.RequestError as e:
            raise HTTPException(
                status_code=503,
                detail="Service unavailable. Could not connect to the weather provider."
            )

    return wrapper
