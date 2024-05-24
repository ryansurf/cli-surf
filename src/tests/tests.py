"""
QA tests
"""

import sys

sys.path.append("..")

import unittest
from unittest.mock import patch
import io
import threading
import requests
import time
import subprocess
import os
from helper import extract_decimal
from api import get_coordinates, get_uv, ocean_information
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
port = int(os.getenv("PORT"))


class TestDecimal(unittest.TestCase):

    def test_invalid_input(self):
        with patch("sys.stdout", new=io.StringIO()) as fake_stdout:
            extract_decimal(["decimal=NotADecimal"])
            printed_output = fake_stdout.getvalue().strip()
            self.assertEqual(
                printed_output, "Invalid value for decimal. Please provide an integer."
            )

    def test_default_input(self):
        decimal = extract_decimal([])
        self.assertEqual(1, decimal)


class TestApis(unittest.TestCase):

    def test_get_coordinates(self):
        coordinates = get_coordinates(["loc=santa_cruz"])
        lat = coordinates[0]
        long = coordinates[1]
        self.assertIsInstance(lat, (int, float))
        self.assertIsInstance(long, (int, float))

    def test_get_uv(self):
        uv = get_uv(37, 122, 2)
        self.assertIsInstance(uv, (int, float))

    def test_ocean_information(self):
        ocean = ocean_information(37, 122, 2)
        self.assertIsInstance(ocean[0], (int, float))
        self.assertIsInstance(ocean[1], (int, float))
        self.assertIsInstance(ocean[2], (int, float))


if __name__ == "__main__":

    unittest.main()
