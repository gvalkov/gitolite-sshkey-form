#!/usr/bin/env python3
# -*- coding: utf-8; -*-

from __future__ import absolute_import
from __future__ import print_function

from websshkey.views import app


class RemoteUserMiddleware:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        user = environ.pop('HTTP_X_PROXY_REMOTE_USER', None)
        environ['REMOTE_USER'] = user
        return self.app(environ, start_response)

class TestUserMiddleware:
    def __init__(self, app, remote_user='joe'):
        self.app = app
        self.remote_user = remote_user

    def __call__(self, environ, start_response):
        environ['REMOTE_USER'] = self.remote_user
        return self.app(environ, start_response)


app.wsgi_app = TestUserMiddleware(app.wsgi_app)
app.wsgi_app = RemoteUserMiddleware(app.wsgi_app)

if __name__ == '__main__':
    app.run(debug=True)
