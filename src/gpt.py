"""
GPT Functions stored here
"""

from g4f.client import Client
from openai import OpenAI


def simple_gpt(surf_summary, gpt_prompt):
    """
    Surf summary is a report of todays data, ex: The surf is 4
    feet with a 10 second period... GPT Prompt is what kind of
    report the user wants, loaded in from the environment vars
    Using: https://github.com/xtekky/gpt4free
    """
    client = Client()
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": surf_summary + gpt_prompt}],
    )
    return response.choices[0].message.content


def openai_gpt(surf_summary, gpt_prompt, api_key, model):
    """
    Surf Summary is a brief summary of the surf data(height, period)
    and gpt_prompt is the personal report the user wants(reccomend a
    board, etc). gpt_prompt in .env
    Uses openai's GPT, needs an API key
    https://platform.openai.com/docs/api-reference/introduction
    """
    client = OpenAI(
        # This is the default and can be omitted
        api_key=api_key,
    )
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
