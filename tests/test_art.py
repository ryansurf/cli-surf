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
    # Color is invalid, should default to blue
    art.print_wave(1, 0, "sdfsd")

    # Reset redirect.
    sys.stdout = sys.__stdout__

    # Now captured_output.getvalue() contains the printed content
    output = captured_output.getvalue()

    # Perform assertions based on expected output
    assert "[0;34m" in output, "Blue color code not found in output"
    assert output, "print_wave() did not print anything"


def test_print_large_wave():
    """print_wave prints the large wave art when show_large_wave is True."""
    captured_output = io.StringIO()
    sys.stdout = captured_output

    art.print_wave(True, True, "blue")

    sys.stdout = sys.__stdout__
    output = captured_output.getvalue()

    assert "[0;34m" in output, "Blue color code not found in large wave output"
    assert output, "print_wave() did not print anything for large wave"
