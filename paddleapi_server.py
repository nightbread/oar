#!/usr/bin/env python
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import argparse
import json
import logging
import ssl
import sys
import urllib.parse
import uuid


class PaddleAPIServerHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        self.send_response(200)
        self.end_headers()
        self.wfile.write('This is an activation server for GPGMail.'.encode())

    def do_POST(self) -> None:
        body = self.rfile.read(int(self.headers['Content-Length'])).decode()
        self.send_response(200)
        self.end_headers()
        request_info = urllib.parse.parse_qs(body)
        self.log_message('Request data:')
        for key in request_info.keys():
            self.log_message('%-32s = %s', key, ' '.join(request_info[key]))
        self.wfile.write(
            json.dumps(
                dict(
                    success=1,
                    response=dict(
                        # Can also be 'feature_license'. Not tested
                        type='activation_license',
                        product_id=request_info['product_id'][0],
                        activation_id=uuid.uuid4().hex,  # Can be anything
                        # If set to 1, 'expiry_date' field is required.
                        # Otherwise, license never expires.
                        expires=0,
                        # expiry_date=time.time() + 24 * 60 * 60 * 365,
                    ))).encode())


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('-k', '--key-file', default='./cert-key.pem')
    parser.add_argument('-c', '--cert-file', default='./cert-crt.pem')
    parser.add_argument('-P', '--port', default=443, type=int)
    parser.add_argument('--ip', default='', metavar='IP')
    args = parser.parse_args()
    httpd = ThreadingHTTPServer((args.ip, args.port), PaddleAPIServerHandler)
    httpd.socket = ssl.wrap_socket(httpd.socket,
                                   keyfile=args.key_file,
                                   certfile=args.cert_file,
                                   server_side=True)
    httpd.serve_forever()
    return 0


if __name__ == '__main__':
    sys.exit(main())
