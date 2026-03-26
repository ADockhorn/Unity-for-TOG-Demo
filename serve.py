"""Local server for testing the immersive article with Unity WebGL build.

Unity WebGL requires proper MIME types and headers for .br (Brotli) files.
Run: python serve.py
Then open: http://localhost:8000
"""

import http.server
import sys

PORT = 8000


class UnityHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        path = self.path.lower()
        if path.endswith(".br"):
            self.send_header("Content-Encoding", "br")
        super().end_headers()

    def guess_type(self, path):
        path = path.lower()
        if path.endswith(".js.br"):
            return "application/javascript"
        if path.endswith(".wasm.br"):
            return "application/wasm"
        if path.endswith(".data.br"):
            return "application/octet-stream"
        return super().guess_type(path)


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else PORT
    with http.server.HTTPServer(("", port), UnityHTTPRequestHandler) as httpd:
        print(f"Serving at http://localhost:{port}")
        httpd.serve_forever()
