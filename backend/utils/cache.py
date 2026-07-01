from datetime import datetime, timezone, timedelta


def is_cache_valid(updated_at: datetime, ttl: timedelta = timedelta(hours=3)) -> bool:
    """
    Evaluates if a given timestamp is still valid based on a Time-To-Live (TTL).
    """
    if not updated_at:
        return False

    now = datetime.now(timezone.utc)
    return (now - updated_at) < ttl
