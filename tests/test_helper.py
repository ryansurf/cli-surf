"""
QA tests for helper.py
Make sure pytest is installed: pip install pytest
Run pytest: pytest
"""

import io
import sys
from unittest.mock import patch

from src.helper import extract_decimal, print_location, set_output_values


def test_invalid_input():
    """
    Test if decimal input prints proper invalid input message
    """
    with patch("sys.stdout", new=io.StringIO()) as fake_stdout:
        extract_decimal(["decimal=NotADecimal"])
        printed_output = fake_stdout.getvalue().strip()
        expected = "Invalid value for decimal. Please provide an integer."
        assert printed_output == expected


def test_default_input():
    """
    Test that when no decimal= in args, 1 is the default
    """
    decimal = extract_decimal([])
    assert 1 == decimal


def test_print_location():
    city = "Perth"
    show_city = 1
    captured_output = io.StringIO()
    sys.stdout = captured_output
    print_location(city, show_city)
    sys.stdout = sys.__stdout__
    expected_output = "Location: Perth"
    assert captured_output.getvalue().strip() == expected_output.strip()


def test_set_output_values():
    args = ['hw', 'show_large_wave', 'huv']
    arguments = {}
    expected = {"show_wave": 0, "show_large_wave": 1, "show_uv": 0}
    assert set_output_values(args, arguments) == expected
