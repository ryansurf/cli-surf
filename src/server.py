"""
Flask Server!
"""

import logging
import subprocess
import sys
import urllib.parse
from pathlib import Path

from flask import (
    Flask,
    render_template,
    request,
    send_file,
    send_from_directory,
)
from flask_cors import CORS

from src.settings import ServerSettings

logger = logging.getLogger(__name__)


def create_app(env):
    """
    Application factory function
    """
    app = Flask(__name__)
    CORS(app)

    @app.route("/help")
    def serve_help():
        """Serves the help.txt file."""
        return send_from_directory(
            Path(__file__).resolve().parents[1], "help.txt"
        )

    @app.route("/home")
    def serve_index():
        """Serves index.html."""
        return render_template("index.html", env_vars=env.model_dump())

    @app.route("/script.js")
    def serve_script():
        """Serves the frontend JavaScript."""
        return send_file("static/script.js")

    @app.route("/")
    def default_route():
        """Serves the surf report."""
        query_parameters = urllib.parse.parse_qsl(
            request.query_string.decode(), keep_blank_values=True
        )
        parsed_parameters = [
            f"{key}={value}" if value else key
            for key, value in query_parameters
        ]
        args = ",".join(parsed_parameters)

        try:
            result = subprocess.run(
                [sys.executable, Path("src") / "cli.py", args],
                capture_output=True,
                text=True,
                check=True,
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            logger.error("Subprocess error: %s", e.stderr)
            raise

    return app


if __name__ == "__main__":  # pragma: no cover
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    env = ServerSettings()
    app = create_app(env)
    app.run(host="0.0.0.0", port=env.PORT, debug=env.DEBUG)
