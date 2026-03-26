from http import HTTPStatus

from fastapi.testclient import TestClient

from src.server import create_app
from src.settings import ServerSettings


def test_root_returns_200():
    env = ServerSettings()
    app = create_app(env)

    client = TestClient(app)
    resp = client.get("/")

    assert resp.status_code == HTTPStatus.OK
    assert "wave" in resp.text.lower()
