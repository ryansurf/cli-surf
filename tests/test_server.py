"""
Tests for server.py
"""

import subprocess
from http import HTTPStatus
from unittest.mock import patch

from src.server import create_app
from src.settings import ServerSettings


def _make_app():
    return create_app(ServerSettings())


def test_serve_index_returns_200(monkeypatch):
    """GET /home renders the index template and returns 200."""
    app = _make_app()
    with patch("src.server.render_template", return_value="<html>home</html>"):
        resp = app.test_client().get("/home")
    assert resp.status_code == HTTPStatus.OK
    assert b"<html>home</html>" in resp.data


def test_serve_script_returns_200(monkeypatch):
    """GET /script.js serves the JavaScript file and returns 200."""
    app = _make_app()
    with patch("src.server.send_file", return_value="console.log('ok')"):
        resp = app.test_client().get("/script.js")
    assert resp.status_code == HTTPStatus.OK


def test_root_subprocess_error_returns_500(monkeypatch):
    """GET / returns 500 and logs the error when the subprocess fails."""
    app = _make_app()

    def fail_run(*args, **kwargs):
        raise subprocess.CalledProcessError(1, "cmd", stderr="boom")

    monkeypatch.setattr(subprocess, "run", fail_run)
    resp = app.test_client().get("/")
    assert resp.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
