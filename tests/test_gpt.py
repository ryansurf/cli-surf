"""
Tests for gpt.py
"""

from unittest.mock import Mock

import pytest

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


def test_free_gpt_returns_model_content(mocker):
    """FreeGpt.call_llm returns the text content from the g4f response."""
    mock_client = Mock()
    mock_client.chat.completions.create.return_value = _make_chat_response(
        "Great surf day!"
    )
    mocker.patch("g4f.client.Client", return_value=mock_client)

    result = gpt.FreeGpt("gpt-3.5-turbo").call_llm("surf is 4ft")

    assert result == "Great surf day!"
    mock_client.chat.completions.create.assert_called_once()


def test_free_gpt_raises_on_exception(mocker):
    """FreeGpt.call_llm propagates exceptions to the caller."""
    mock_client = Mock()
    mock_client.chat.completions.create.side_effect = Exception("API down")
    mocker.patch("g4f.client.Client", return_value=mock_client)

    llm = gpt.FreeGpt("gpt-3.5-turbo")
    with pytest.raises(Exception, match="API down"):
        llm.call_llm("surf is 4ft")


def test_openai_llm_returns_model_content(mocker):
    """OpenAILlm.call_llm returns the text content from the OpenAI response."""
    mock_client = Mock()
    mock_client.chat.completions.create.return_value = _make_chat_response(
        "Bring your longboard."
    )
    mocker.patch("src.gpt.OpenAI", return_value=mock_client)

    result = gpt.OpenAILlm("sk-testkey", "gpt-4").call_llm("surf is 2ft")

    assert result == "Bring your longboard."
    mock_client.chat.completions.create.assert_called_once()


def test_openai_llm_raises_on_exception(mocker):
    """OpenAILlm.call_llm propagates exceptions to the caller."""
    mock_client = Mock()
    mock_client.chat.completions.create.side_effect = Exception(
        "quota exceeded"
    )
    mocker.patch("src.gpt.OpenAI", return_value=mock_client)

    llm = gpt.OpenAILlm("sk-key", "gpt-4")
    with pytest.raises(Exception, match="quota exceeded"):
        llm.call_llm("surf is 2ft")
