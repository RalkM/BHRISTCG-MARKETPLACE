"""This will be storing API results temporarily so that we are not overloading requests to Pokemon TCG API. This is a simple in-memory cache, and it will be cleared when the application restarts."""
import time
from typing import Any, Optional

_cache: dict = {}


def get(key: str) -> Optional[Any]:
    if key not in _cache:
        return None
    value, expires_at = _cache[key]
    if time.time() > expires_at:
        del _cache[key]
        return None
    return value


def set(key: str, value: Any, ttl: int = 3600) -> None:
    _cache[key] = (value, time.time() + ttl)


def delete(key: str) -> None:
    _cache.pop(key, None)


def has(key: str) -> bool:
    return get(key) is not None
