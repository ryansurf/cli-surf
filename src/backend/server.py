"""
Flask Server!
"""

from flask import Flask, send_file, send_from_directory, request
import subprocess
import json
import helper
import sys
import asyncio
import urllib.parse

app = Flask(__name__)

with open('../../config.json') as f:
    json_config = json.load(f)

port_json = int(json_config["server"]["port"])

@app.route('/config.json')
def serve_config():
    return send_from_directory('../../', 'config.json')

@app.route('/help')
def serve_help():
    return send_from_directory('../../', 'help.txt')

@app.route('/home')
def serve_index():
    return send_file('../frontend/index.html')

@app.route('/script.js')
def serve_script():
    return send_file('../frontend/script.js')

@app.route('/')
def default_route():
    query_parameters = urllib.parse.parse_qsl(request.query_string.decode(), keep_blank_values=True)
    parsed_parameters = []

    for key, value in query_parameters:
        if value:
            parsed_parameters.append(f"{key}={value}")
        else:
            parsed_parameters.append(key)

    # Join the parsed parameters list into a single string
    args = ','.join(parsed_parameters)

    async def run_subprocess():
        result = subprocess.run(
            ["python3", "main.py", args],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout

    # Run subprocess asynchronously
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(run_subprocess())
    return result

if __name__ == '__main__':
    app.run(port=port_json)