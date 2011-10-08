#!/usr/bin/env python
# encoding: utf-8

from os.path import abspath, dirname,join
from os import environ

config = join(abspath(dirname(__file__)), '../etc/test-config.py')
environ['WEBSSHKEY_HELPER_CONFIG'] = config

from websshkey.app import app

def TestMiddleware(app):
    def inner(environ, start_response):
        environ['REMOTE_USER'] = 'johndoe'
        return app(environ, start_response)
    return inner

app.wsgi_app = TestMiddleware(app.wsgi_app)
app.run(debug=True)
