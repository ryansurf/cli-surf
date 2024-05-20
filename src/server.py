import http.server
import subprocess
from urllib.parse import urlparse, parse_qs
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
port = int(os.getenv('PORT'))

class MyHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        # Parse the query parameters
        parsed_url = urlparse(self.path)
        query_params = parse_qs(parsed_url.query)

        # Extract the arguments from the query parameters
        args = query_params.get('args', [])

        if 'help' in args:
            # If 'help' is in the args, read and return the content of help.txt
            try:
                with open('../help.txt', 'r') as file:
                    help_text = file.read()
                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(help_text.encode())
            except FileNotFoundError:
                self.send_response(404)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(b"help.txt not found")
        else:
            # Otherwise, run the main.py script with the provided arguments
            result = subprocess.run(['python3', 'main.py'] + args, capture_output=True, text=True)
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(result.stdout.encode())

def run(server_class=http.server.HTTPServer, handler_class=MyHTTPRequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Server running on port {port}")
    httpd.serve_forever()

if __name__ == '__main__':
    run(port=port)
