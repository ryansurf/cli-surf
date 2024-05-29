"""
Flask Server!
"""

import asyncio
import subprocess
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
from settings import ServerSettings

# Load environment variables from .env file
env = ServerSettings()

app = Flask(__name__)
CORS(app)


@app.route("/help")
def serve_help():
    return send_from_directory(f"{str(Path(__file__).parent)}/", "help.txt")


@app.route("/home")
def serve_index():
    return render_template("index.html", env_vars=env.model_dump())


@app.route("/script.js")
def serve_script():
    return send_file("static/script.js")


@app.route("/")
def default_route():
    query_parameters = urllib.parse.parse_qsl(
        request.query_string.decode(), keep_blank_values=True
    )
    parsed_parameters = []

    for key, value in query_parameters:
        if value:
            parsed_parameters.append(f"{key}={value}")
        else:
            parsed_parameters.append(key)

    # Join the parsed parameters list into a single string
    args = ",".join(parsed_parameters)

    async def run_subprocess():
        try:
            result = subprocess.run(
                ["python3", "cli.py", args],
                capture_output=True,
                text=True,
                check=True,
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            # Print the error message from the subprocess
            print("Error message from subprocess:", e.stderr)
            # Raise the error again to propagate it
            raise e

    # Run subprocess asynchronously
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(run_subprocess())
    return result


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=env.PORT)
