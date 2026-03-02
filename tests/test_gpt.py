"""
Tests for gpt.py
"""

from unittest.mock import Mock

from src import gpt


def _make_chat_response(content):
    """Build a minimal chat completion response mock."""
    message = Mock()
    message.content = content
    choice = Mock()
    choice.message = message
    response = Mock()
    response.choices = [choice]
    return response


def test_simple_gpt_returns_model_content(mocker):
    """simple_gpt returns the text content from the g4f response."""
    mock_client = Mock()
    mock_client.chat.completions.create.return_value = _make_chat_response(
        "Great surf day!"
    )
    mocker.patch("src.gpt.Client", return_value=mock_client)

    result = gpt.simple_gpt("surf is 4ft", "what board should I ride?")

    assert result == "Great surf day!"
    mock_client.chat.completions.create.assert_called_once()


def test_simple_gpt_returns_fallback_on_exception(mocker):
    """simple_gpt returns the error string when the g4f client raises."""
    mocker.patch("src.gpt.Client", side_effect=Exception("API down"))

    result = gpt.simple_gpt("surf is 4ft", "what board?")

    assert result == "Unable to generate GPT response."


def test_openai_gpt_returns_model_content(mocker):
    """openai_gpt returns the text content from the OpenAI response."""
    mock_client = Mock()
    mock_client.chat.completions.create.return_value = _make_chat_response(
        "Bring your longboard."
    )
    mocker.patch("src.gpt.OpenAI", return_value=mock_client)

    result = gpt.openai_gpt(
        "surf is 2ft", "recommend a board", "sk-testkey", "gpt-4"
    )

    assert result == "Bring your longboard."
    mock_client.chat.completions.create.assert_called_once()


def test_openai_gpt_returns_fallback_on_exception(mocker):
    """openai_gpt returns the error string when the OpenAI client raises."""
    mocker.patch("src.gpt.OpenAI", side_effect=Exception("quota exceeded"))

    result = gpt.openai_gpt(
        "surf is 2ft", "recommend a board", "sk-key", "gpt-4"
    )

    assert result == "Unable to generate GPT response."
