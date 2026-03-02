"""
Tests for send_email.py
"""

import subprocess
from unittest.mock import MagicMock

from src.send_email import send_user_email


def _env_defaults():
    return {
        "EMAIL": "sender@example.com",
        "EMAIL_RECEIVER": "receiver@example.com",
        "SUBJECT": "Surf Report",
        "COMMAND": "localhost:8000",
        "SMTP_SERVER": "smtp.example.com",
        "SMTP_PORT": 587,
        "EMAIL_PW": "secret",
    }


def _patch_env(mocker, **overrides):
    env = _env_defaults()
    env.update(overrides)
    return mocker.patch(
        "src.send_email.EmailSettings", return_value=MagicMock(**env)
    )


def test_send_email_success(mocker):
    """send_user_email fetches the report via curl and sends the email."""
    _patch_env(mocker)

    mock_result = MagicMock()
    mock_result.stdout = "Surf height: 3ft"
    mocker.patch("subprocess.run", return_value=mock_result)

    mock_smtp = MagicMock()
    mock_smtp_cls = mocker.patch("smtplib.SMTP", return_value=mock_smtp)
    mock_smtp.__enter__ = lambda s: s
    mock_smtp.__exit__ = MagicMock(return_value=False)

    send_user_email()

    mock_smtp_cls.assert_called_once()
    mock_smtp.sendmail.assert_called_once()


def test_send_email_curl_failure_uses_fallback_body(mocker):
    """send_user_email falls back to an error message when curl fails."""
    _patch_env(mocker)

    mocker.patch(
        "subprocess.run",
        side_effect=subprocess.CalledProcessError(1, "curl", stderr="error"),
    )

    mock_smtp = MagicMock()
    mocker.patch("smtplib.SMTP", return_value=mock_smtp)
    mock_smtp.__enter__ = lambda s: s
    mock_smtp.__exit__ = MagicMock(return_value=False)

    # Should not raise; the fallback body is used instead
    send_user_email()

    mock_smtp.sendmail.assert_called_once()
    # The email body should contain the fallback message
    call_args = mock_smtp.sendmail.call_args[0]
    assert "Failed to fetch surf report." in call_args[2]
