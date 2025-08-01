# server.py
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import threading

PORT = 8000  # must match your REDIRECT_URI port

class OAuthCallbackHandler(BaseHTTPRequestHandler):
    # Shared global variable to store the latest received auth code
    auth_code = None

    def do_GET(self):
        parsed_path = urlparse(self.path)
        if parsed_path.path == '/callback':
            query = parse_qs(parsed_path.query)
            code = query.get('code')
            if code:
                OAuthCallbackHandler.auth_code = code[0]
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b"<html><body><h2>Login successful! You may close this window.</h2")

                self.wfile.write(b"</body></html>")
                print(f"Received auth code: {code[0]}")  # Print the code to console
            else:
                self.send_error(400, "Missing code parameter.")
        else:
            self.send_error(404)

    def log_message(self, format, *args):
        # Suppress default logging
        return

def run_server():
    server_address = ('', PORT)
    httpd = HTTPServer(server_address, OAuthCallbackHandler)
    print(f"Server started on http://localhost:{PORT}, waiting for callbacks...")
    httpd.serve_forever()  # Handle requests indefinitely

if __name__ == "__main__":
    run_server()
