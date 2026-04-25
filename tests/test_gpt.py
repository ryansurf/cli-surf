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


def test_free_gpt_returns_model_content(mocker):
    """FreeGpt.call_llm returns the text content from the g4f response."""
    mock_client = Mock()
    mock_client.chat.completions.create.return_value = _make_chat_response(
        "Great surf day!"
    )
    mocker.patch("src.gpt.Client", return_value=mock_client)

    result = gpt.FreeGpt("gpt-3.5-turbo").call_llm(
        "surf is 4ft", "what board should I ride?"
    )

    assert result == "Great surf day!"
    mock_client.chat.completions.create.assert_called_once()


def test_free_gpt_returns_fallback_on_exception(mocker):
    """FreeGpt.call_llm returns the error string when the client raises."""
    mock_client = Mock()
    mock_client.chat.completions.create.side_effect = Exception("API down")
    mocker.patch("src.gpt.Client", return_value=mock_client)

    result = gpt.FreeGpt("gpt-3.5-turbo").call_llm(
        "surf is 4ft", "what board?"
    )

    assert result == "Unable to generate GPT response."


def test_openai_llm_returns_model_content(mocker):
    """OpenAILlm.call_llm returns the text content from the OpenAI response."""
    mock_client = Mock()
    mock_client.chat.completions.create.return_value = _make_chat_response(
        "Bring your longboard."
    )
    mocker.patch("src.gpt.OpenAI", return_value=mock_client)

    result = gpt.OpenAILlm("sk-testkey", "gpt-4").call_llm(
        "surf is 2ft", "recommend a board"
    )

    assert result == "Bring your longboard."
    mock_client.chat.completions.create.assert_called_once()


def test_openai_llm_returns_fallback_on_exception(mocker):
    """OpenAILlm.call_llm returns the error string when the client raises."""
    mock_client = Mock()
    mock_client.chat.completions.create.side_effect = Exception(
        "quota exceeded"
    )
    mocker.patch("src.gpt.OpenAI", return_value=mock_client)

    result = gpt.OpenAILlm("sk-key", "gpt-4").call_llm(
        "surf is 2ft", "recommend a board"
    )

    assert result == "Unable to generate GPT response."
