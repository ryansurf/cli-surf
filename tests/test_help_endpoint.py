from http import HTTPStatus

from src.server import create_app
from src.settings import ServerSettings


def test_help_endpoint_returns_200():
    env = ServerSettings()
    app = create_app(env)

    client = app.test_client()
    resp = client.get("/help")

    assert resp.status_code == HTTPStatus.OK
    assert len(resp.data) > 0
