"""
GPT Functions stored here
"""

from g4f.client import Client


def simple_gpt(surf_summary, gpt_prompt):
    """
    Surf summary is a report of todays data, ex: The surf is 4
    feet with a 10 second period... GPT Prompt is what kind of
    report the user wants, loaded in from the environment vars
    """
    client = Client()
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": surf_summary + gpt_prompt}],
    )
    return response.choices[0].message.content
