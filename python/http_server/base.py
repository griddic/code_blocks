import random
import time
from http.server import HTTPServer, BaseHTTPRequestHandler


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def __init__(self):
        super().__init__(self)
        self.cocounter = 0

    def do_GET(self):
        self.cocounter += 1
        try:
            self.send_response(200)
            self.end_headers()
            time.sleep(random.randint(1, 3))
            self.wfile.write(f'cocounter = {self.cocounter}'.encode('utf-8'))
        finally:
            self.cocounter -= 1


if __name__ == '__main__':
    httpd = HTTPServer(('localhost', 8000), SimpleHTTPRequestHandler)
    httpd.serve_forever()
