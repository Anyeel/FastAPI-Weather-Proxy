from fastapi import HTTPException


def parse_comma_separated_cities(cities: str) -> list[int]:
    """
    Parses a comma-separated string of IDs into a list of integers.
    """
    try:
        return [int(cid.strip()) for cid in cities.split(",") if cid.strip()]
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid format. City IDs must be integers separated by commas."
        )
