"""
Code-demo demowsgi server, web app & middleware
https://rahmonov.me/posts/what-the-hell-is-wsgi-anyway-and-what-do-you-eat-it-with/
"""

import time
from wsgiref.simple_server import make_server


def application(environ, start_response):
    resp_body = str(time.time()) + '\n' + _get_resp_str(environ)
    status = '200 OK'
    resp_headers = [
        ('Content-type', 'text/plain'),
    ]
    start_response(status, resp_headers)
    return [resp_body.encode('utf-8')]


def _get_resp_str(environ):
    return '\n'.join([f'{key}: {val}' for key, val in sorted(environ.items())])


class Reverseware:
    def __init__(self, app):
        self.wrapped_app = app

    def __call__(self, environ, start_response):
        return [data[::-1] for data in self.wrapped_app(environ, start_response)]


if __name__ == '__main__':
    server = make_server('localhost', 8001, app=Reverseware(application))
    server.serve_forever()
