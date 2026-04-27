"""
GPT Functions stored here
"""

import io
import logging
from contextlib import redirect_stdout
from functools import lru_cache

from openai import OpenAI

from src import settings

logger = logging.getLogger(__name__)

MIN_KEY_LEN = 5

gpt_env = settings.GPTSettings()


class Llm:
    def __init__(self, model):
        self.model = model
        self.prompt = gpt_env.GPT_PROMPT

    def call_llm(self, surf_summary) -> str | None:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": surf_summary + self.prompt}],
        )
        return response.choices[0].message.content


class FreeGpt(Llm):
    def __init__(self, model):
        from g4f.client import Client  # noqa: PLC0415

        super().__init__(model)
        self.client = Client()

    def call_llm(self, surf_summary) -> str | None:
        with redirect_stdout(io.StringIO()):
            return super().call_llm(surf_summary)


class OpenAILlm(Llm):
    def __init__(self, api_key, model):
        super().__init__(model)
        self.client = OpenAI(api_key=api_key)


def _create_llm_client() -> Llm:
    gpt_api_key = gpt_env.API_KEY
    gpt_model = gpt_env.GPT_MODEL
    if not gpt_api_key or len(gpt_api_key) < MIN_KEY_LEN:
        return FreeGpt(gpt_model)
    return OpenAILlm(api_key=gpt_api_key, model=gpt_model)


@lru_cache(maxsize=1)
def get_llm_client() -> Llm:
    return _create_llm_client()
