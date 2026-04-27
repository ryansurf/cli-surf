"""
Pytest configuration and shared fixtures.
"""

from unittest.mock import MagicMock, patch

# Prevent g4f from loading its C extensions (curl_cffi/eventlet) during tests,
# which cause segfaults when mixed with the test runner's event loop.
patch("g4f.client.Client", MagicMock()).start()
