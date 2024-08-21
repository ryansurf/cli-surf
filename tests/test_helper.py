"""
QA tests for helper.py
Make sure pytest is installed: pip install pytest
Run pytest: pytest
"""

import io
from unittest.mock import patch

from src import cli, helper


def test_invalid_input():
    """
    Test if decimal input prints proper invalid input message
    """
    with patch("sys.stdout", new=io.StringIO()) as fake_stdout:
        helper.extract_decimal(["decimal=NotADecimal"])
        printed_output = fake_stdout.getvalue().strip()
        expected = "Invalid value for decimal. Please provide an integer."
        assert printed_output == expected


def test_default_input():
    """
    Test that when no decimal= in args, 1 is the default
    """
    decimal = helper.extract_decimal([])
    assert 1 == decimal


def test_json_output():
    """
    Passing "JSON" as an argument to cli.run,
    we check if a JSON object returns.
    We also check for expected outputs,
    like a lat that is a float/int
    """
    # Hardcode lat and long for location.
    # If not, when test are ran in Github Actions
    # We get an error(because server probably isn't near ocean)
    json_output = cli.run(36.95, -121.97, ["", "json"])
    assert type(json_output["Lat"]) in {int, float}
    assert isinstance(json_output["Location"], str)


def test_print_gpt():
    """
    Tests the simple_gpt()
    """
    surf_data = {
        "Location": "test",
        "Height": "test",
        "Swell Direction": "test",
        "Period": "test",
        "Unit": "test",
    }
    gpt_prompt = "Please output 'gpt works'"
    gpt_info = [None, ""]
    gpt_response = helper.print_gpt(surf_data, gpt_prompt, gpt_info)
    assert "gpt works" in gpt_response
