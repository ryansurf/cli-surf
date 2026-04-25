"""
GPT Functions stored here
"""

import logging
from abc import ABC
from typing import Any

from g4f.client import Client
from openai import OpenAI

logger = logging.getLogger(__name__)


class Llm(ABC):

    def __init__(self, model):
        self.model = model
        self.client: Any = None

    def call_llm(self, surf_summary, gpt_prompt) -> str | None:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": surf_summary + gpt_prompt}],
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error("LLM request failed: %s", e)
            return "Unable to generate GPT response."


class FreeGpt(Llm):
    def __init__(self, model):
        super().__init__(model)
        self.client = Client()


class OpenAILlm(Llm):
    def __init__(self, api_key, model):
        super().__init__(model)
        self.client = OpenAI(api_key=api_key)
