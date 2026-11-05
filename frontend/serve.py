"""Servidor estático del frontend (sin build). Uso: python serve.py  ->  http://127.0.0.1:9988"""
import http.server
import os
import socketserver
from functools import partial

HOST = os.getenv("FRONTEND_HOST", "127.0.0.1")
PORT = int(os.getenv("FRONTEND_PORT", "9988"))
DIRECTORY = os.path.dirname(os.path.abspath(__file__))


class Handler(http.server.SimpleHTTPRequestHandler):
    # En Windows el registro puede mapear .js a text/plain y romper los ES modules.
    extensions_map = {
        **http.server.SimpleHTTPRequestHandler.extensions_map,
        ".js": "text/javascript",
        ".css": "text/css",
        ".html": "text/html",
    }

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()


class Server(socketserver.ThreadingMixIn, http.server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True


if __name__ == "__main__":
    with Server((HOST, PORT), partial(Handler, directory=DIRECTORY)) as httpd:
        print(f"[INFO] Frontend en http://{HOST}:{PORT}")
        httpd.serve_forever()
