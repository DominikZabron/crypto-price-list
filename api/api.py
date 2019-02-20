import json
import logging
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

from db import Storage

SERVER_HOST = os.getenv('SERVER_HOST', '0.0.0.0')
SERVER_PORT = int(os.getenv('SERVER_PORT', '8000'))
DEFAULT_LIMIT = int(os.getenv('DEFAULT_LIMIT', '10'))

db = Storage()


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            qs = parse_qs(urlparse(self.path).query)
            limit = qs.get('limit', (0,))[0] or DEFAULT_LIMIT
            data = db.get_ranked_prices(limit)
            self.send_response(200)
            self._add_headers()
            self.wfile.write(bytes(json.dumps(data), 'utf-8'))
        except Exception as e:
            self._handle_exception(e)

    def do_PUT(self):
        try:
            data = json.loads(self.rfile.read(int(self.headers.get('content-length'))))

            if self.path == '/prices':
                db.update_prices(data)
                self.send_response(204)
            elif self.path == '/ranks':
                db.update_ranks(data)
                self.send_response(204)
            else:
                self.send_response(404)

            self._add_headers()

        except Exception as e:
            self._handle_exception(e)

    def _add_headers(self):
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def _handle_exception(self, exc):
        logging.exception(exc)
        self.send_response(500)
        self._add_headers()
        self.wfile.write(bytes(json.dumps(
            {'error': '{}: {}'.format(type(exc).__name__, str(exc))}), 'utf-8'))


if __name__ == '__main__':
    server_address = (SERVER_HOST, SERVER_PORT)
    httpd = HTTPServer(server_address, RequestHandler)
    httpd.serve_forever()