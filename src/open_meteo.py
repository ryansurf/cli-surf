import requests
import openmeteo_requests
from retry_requests import retry


def _create_client() -> openmeteo_requests.Client:
    """Creates a retry-enabled Open-Meteo API client."""
    retry_session = retry(requests.Session(), retries=5, backoff_factor=0.2)
    return openmeteo_requests.Client(session=retry_session)


openmeteo_client = _create_client()
