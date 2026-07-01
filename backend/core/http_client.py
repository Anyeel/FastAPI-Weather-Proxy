from typing import AsyncGenerator

import httpx


async def get_client() -> AsyncGenerator[httpx.AsyncClient, None]:
    """
    Provides a single instance of httpx.AsyncClient for making HTTP requests.

    It safely opens the connection and ensures it is properly closed after the request finishes.
    """
    async with httpx.AsyncClient() as client:
        yield client
