"""
QA tests for gpt.py
Make sure pytest is installed: pip install pytest
Run pytest: pytest
"""

from src import gpt


def test_simple_gpt():
    """
    Testing the simple_gpt function
    Calls the simple gpt and asks it to output
    "gpt works". If anything else is outputted, we can
    assume an error has occured
    """
    surf_summary = "Please respond with the exact phrase 'gpt works'. Do not include any additional text or context."
    gpt_prompt = "This is for testing purposes"
    gpt_response = gpt.simple_gpt(surf_summary, gpt_prompt)
    assert "gpt works" in gpt_response, f"Expected 'gpt works', but got: {gpt_response}"
