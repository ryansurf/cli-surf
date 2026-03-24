"""
Tests for server.py
"""

import subprocess
from http import HTTPStatus
from unittest.mock import patch

from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.server import create_app
from src.settings import ServerSettings


def _make_app():
    return create_app(ServerSettings())


def test_root_subprocess_error_returns_500(monkeypatch):
    """GET / returns 500 and logs the error when the subprocess fails."""
    app = _make_app()

    def fail_run(*args, **kwargs):
        raise subprocess.CalledProcessError(1, "cmd", stderr="boom")

    monkeypatch.setattr(subprocess, "run", fail_run)
    resp = TestClient(app).get("/")
    assert resp.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
