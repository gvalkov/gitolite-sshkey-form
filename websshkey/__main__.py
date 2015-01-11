#!/usr/bin/env python3
# -*- coding: utf-8; -*-

from __future__ import absolute_import
from __future__ import print_function

import os, sys
from optparse import OptionParser
from websshkey.views import app


#-----------------------------------------------------------------------------
usage = '''\
Usage: websshkey [options]

Webapp for collecting and managing ssh public keys.

Options:
  -h, --help                  show this help message and exit
  -d, --debug                 show debug messages
  -v, --version               show program's version number and exit
  -b, --bind <addr:port>      listen on the specified address and port
  -r, --relative-root <path>  webapp root path (default: /)
  -c, --config-file <path>    read options from config file (optional)

Webapp Options:
  -a, --admin-repo <url>

  The gitolite-admin repository url to clone (optional).

  -w, --workdir <path>

  If '--admin-repo' is set, '--workdir' is the checkout location
  (the working copy) of the '--admin-repo' url. When a key is added
  or removed, the webapp will commit and push to '--admin-repo'.

  If '--admin-repo' is not set (or set to ''), '--workdir' will be
  treated as a plain directory in which public keys are stored.

  -b, --branch <name>

  The gitolite-admin branch to which keys should be pushed.
  Defaults to 'master'.

  -u, --author-name <name>

  Author to use when adding keys to gitolite-admin.
  Defaults to 'Gitolite Publickey Form'.

  -e, --author-email <email>

  Email to use when adding keys to gitolite-admin.
  Defaults to 'nobody@localhost'.

Example Config File:
  ADMIN_REPO   = 'https://url.to/gitolite-admin'
  WORKDIR      = '/path/to/wc'
  BRANCH       = 'master'
  AUTHOR_NAME  = 'Gitolite Public Key Form'
  AUTHOR_EMAIL = '<nobody@localhost>'\
'''

def parseopts(args=sys.argv):
    parser = OptionParser

#-----------------------------------------------------------------------------
# Middlewares
#-----------------------------------------------------------------------------
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

print(usage)
