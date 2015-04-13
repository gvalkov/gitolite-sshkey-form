#!/usr/bin/env python3
# -*- coding: utf-8; -*-

from __future__ import absolute_import
from __future__ import print_function

import os, sys
from optparse import OptionParser
from websshkey.views import app, configure
from websshkey import __version__


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
  -t, --test-user <user>      hardcode REMOTE_USER (useful for testing)

Webapp Options:
  -a, --admin-repo <url>

  The gitolite-admin repository url to clone (optional).

  -w, --workdir <path>

  If '--admin-repo' is set, '--workdir' is the checkout location
  (the working copy) of the '--admin-repo' url. When a key is added
  or removed, the webapp will commit and push to '--admin-repo'.

  If '--admin-repo' is not set (or set to ''), '--workdir' will be
  treated as a plain directory in which public keys are stored.

  -n, --branch <name>

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

#-----------------------------------------------------------------------------
def parseopts(args=sys.argv[1:]):
    parser = OptionParser(usage=usage, add_help_option=False)
    o = parser.add_option
    o('-h', '--help', action='store_true')
    o('-d', '--debug', action='store_true')
    o('-v', '--version', action='store_true')
    o('-b', '--bind', default='localhost:8000')
    o('-r', '--relative-root')
    o('-t', '--test-user')
    o('-c', '--config-file')
    o('-a', '--admin-repo')
    o('-w', '--workdir')
    o('-n', '--branch')
    o('-u', '--author-name')
    o('-e', '--author-email')

    opts, args = parser.parse_args(args)
    return opts, args

def parseaddr(arg):
    tmp = arg.split(':')
    port = int(tmp[-1])
    addr = ''.join(tmp[:-1])
    addr = '' if addr == '*' else addr
    return port, addr

#-----------------------------------------------------------------------------
def main(args=sys.argv):
    opts, args = parseopts(args[1:])

    if opts.help:
        print(usage)
        sys.exit(0)

    if opts.version:
        print('web-sshkey-helper version %s' % __version__)
        sys.exit(0)

    if not opts.config_file:
        class config:
            ADMIN_REPO = opts.admin_repo
            WORKDIR = opts.workdir
            BRANCH  = opts.branch
            AUTHOR_NAME = opts.author_name
            AUTHOR_EMAIL = opts.author_email
        app.config.from_object(config)
    else:
        app.config.from_pyfile(opts.config_file)

    port, addr = parseaddr(opts.bind)

    if opts.test_user:
        app.wsgi_app = TestUserMiddleware(app.wsgi_app, opts.test_user)
    else:
        app.wsgi_app = RemoteUserMiddleware(app.wsgi_app)

    configure()
    app.run(host=addr, port=port, debug=opts.debug)


if __name__ == '__main__':
    main()
