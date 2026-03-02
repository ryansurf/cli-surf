"""
GPT Functions stored here
"""

import logging

from g4f.client import Client
from openai import OpenAI

logger = logging.getLogger(__name__)


def simple_gpt(surf_summary, gpt_prompt):
    """
    Surf summary is a report of todays data, ex: The surf is 4
    feet with a 10 second period... GPT Prompt is what kind of
    report the user wants, loaded in from the environment vars
    Using: https://github.com/xtekky/gpt4free
    """
    try:
        client = Client()
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": surf_summary + gpt_prompt}],
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error("GPT (free) request failed: %s", e)
        return "Unable to generate GPT response."


def openai_gpt(surf_summary, gpt_prompt, api_key, model):
    """
    Surf Summary is a brief summary of the surf data(height, period)
    and gpt_prompt is the personal report the user wants(reccomend a
    board, etc). gpt_prompt in .env
    Uses openai's GPT, needs an API key
    https://platform.openai.com/docs/api-reference/introduction
    """
    try:
        client = OpenAI(api_key=api_key)
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": surf_summary + gpt_prompt,
                }
            ],
            model=model,
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        logger.error("OpenAI request failed: %s", e)
        return "Unable to generate GPT response."
