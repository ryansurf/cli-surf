import sqlite3
import threading

import openmeteo_requests
import requests_cache
from retry_requests import retry

_CACHE_PATH = "/tmp/.cache"
_thread_local = threading.local()


def _build_client() -> openmeteo_requests.Client:
    backend = requests_cache.SQLiteCache(
        _CACHE_PATH, use_memory=False, wal=True
    )
    session = requests_cache.CachedSession(backend=backend, expire_after=3600)
    return openmeteo_requests.Client(
        session=retry(session, retries=5, backoff_factor=0.2)
    )


def _get_thread_client() -> openmeteo_requests.Client:
    if not hasattr(_thread_local, "client"):
        _thread_local.client = _build_client()
    return _thread_local.client


class _ResilientClient:
    def weather_api(self, url, params=None):
        client = _get_thread_client()
        try:
            return client.weather_api(url, params=params)
        except sqlite3.DatabaseError:
            _thread_local.client = _build_client()
            return _thread_local.client.weather_api(url, params=params)


openmeteo_client = _ResilientClient()
