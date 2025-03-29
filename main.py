from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import hashlib
import urllib.parse
from typing import Dict

# Dictionary to store URL mappings
url_mappings: Dict[str, str] = {}

class URLShortenerHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/':
            # Read the request body
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            
            try:
                # Generate a short URL ID using hash
                url_hash = hashlib.md5(post_data.encode()).hexdigest()[:8]
                
                # Store the mapping
                url_mappings[url_hash] = post_data
                
                # Send response
                self.send_response(201)
                self.send_header('Content-Type', 'text/plain')
                self.end_headers()
                self.wfile.write(f"http://127.0.0.1:8080/{url_hash}".encode())
                
            except Exception as e:
                self.send_error(400, f"Bad Request: {str(e)}")
    
    def do_GET(self):
        if self.path == '/':
            self.send_error(400, "Bad Request: No URL ID provided")
            return
            
        # Extract URL ID from path
        url_id = self.path[1:]  # Remove leading '/'
        
        if url_id in url_mappings:
            original_url = url_mappings[url_id]
            self.send_response(307)
            self.send_header('Location', original_url)
            self.end_headers()
        else:
            self.send_error(404, "URL not found")

def run_server(host: str = "127.0.0.1", port: int = 8080):
    server_address = (host, port)
    httpd = HTTPServer(server_address, URLShortenerHandler)
    print(f"Starting server on http://{host}:{port}")
    httpd.serve_forever()

if __name__ == "__main__":
    run_server()
