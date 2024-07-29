"""
QA tests for server.py
Make sure pytest is installed: pip install pytest
Run pytest: pytest
"""

from src.server import create_app


def test_routes():
    """
    Test that the routes are able to be retrieved
    /home, /help, /
    When a page is requested (GET)
    THEN check if the response is valid (200)
    """
    env = ServerSettings()
    flask_app = create_app(env)
    OK = 200

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as test_client:
        response_help = test_client.get("/help")
        assert response_help.status_code == OK

        response_home = test_client.get("/home")
        assert response_home.status_code == OK

        response_root = test_client.get("/")
        assert response_root.status_code == OK
