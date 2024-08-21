"""
QA tests for art.py
Make sure pytest is installed: pip install pytest
Run pytest: pytest
"""

import io
import sys

from src import art


def test_print_wave():
    """
    Testing the print_wave() function
    Uses sys & io to capture printed output
    """
    # Capture the output
    captured_output = io.StringIO()  # Create StringIO object
    sys.stdout = captured_output  # Redirect stdout.

    # Call the function
    art.print_wave(1, 0, "blue")

    # Reset redirect.
    sys.stdout = sys.__stdout__

    # Now captured_output.getvalue() contains the printed content
    output = captured_output.getvalue()

    # Perform assertions based on expected output
    assert output
