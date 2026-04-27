import openmeteo_requests
import requests_cache
from retry_requests import retry


def _create_client() -> openmeteo_requests.Client:
    """Creates a cached, retry-enabled Open-Meteo API client."""
    backend = requests_cache.SQLiteCache(
        "/tmp/.cache", use_memory=False, wal=True
    )
    cache_session = requests_cache.CachedSession(
        backend=backend, expire_after=3600
    )
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    return openmeteo_requests.Client(session=retry_session)


openmeteo_client = _create_client()
