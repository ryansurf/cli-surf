import subprocess
from http import HTTPStatus

from src.server import create_app
from src.settings import ServerSettings


def test_root_returns_200_with_mock(monkeypatch):
    env = ServerSettings()
    app = create_app(env)

    class DummyCompleted:
        stdout = "ok"
        stderr = ""

    def fake_run(*args, **kwargs):
        return DummyCompleted()

    monkeypatch.setattr(subprocess, "run", fake_run)

    client = app.test_client()
    resp = client.get("/")

    assert resp.status_code == HTTPStatus.OK
    assert b"ok" in resp.data
