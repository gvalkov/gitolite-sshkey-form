# -*- coding: utf-8; -*-

from __future__ import absolute_import
from __future__ import print_function

import os, sys

import flask
import base64
import logging

from websshkey import backends
from websshkey import utils

#-----------------------------------------------------------------------------
log = logging.getLogger()
app = flask.Flask(__name__)

#-----------------------------------------------------------------------------
# Read config from environment
#-----------------------------------------------------------------------------
app.config.from_envvar('WEBSSHKEY_CONFIG')

config = app.config.get
author_name       = config('AUTHOR_NAME', 'Gitolite Publickey Form')
author_email      = config('AUTHOR_EMAIL' 'nobody@localhost')
admin_repo_url    = config('ADMIN_REPO', '')
admin_repo_branch = config('BRANCH', 'master')
workdir           = config('WORKDIR')

if not workdir:
    print('Please set WORKDIR in %s' % os.environ['WEBSSHKEY_CONFIG'], file=sys.stderr)
    sys.exit(1)

#-----------------------------------------------------------------------------
repo = None
if admin_repo_url:
    pass
else:
    repo = backends.Directory(workdir)


#-----------------------------------------------------------------------------
@app.route('/', methods=['GET'])
def index():
    remote_user = flask.request.environ['REMOTE_USER']
    keys = repo.listkeys(remote_user)
    keys = utils.listkeys64(keys)

    ctx = {
        'remote_user': remote_user,
        'sshkeys': list(keys),
        'enable_identities': app.config.get('ENABLE_IDENTITIES')
    }

    return flask.render_template('index.jinja', **ctx)

#-----------------------------------------------------------------------------
@app.route('/add', methods=['POST'])
def addkey():
    remote_user = flask.request.environ['REMOTE_USER']
    key = flask.request.form.get('data')

    if not key:
        return flask.Response('Empty public key', status=400)

    if not utils.iskeyvalid(key):
        return flask.Response('Invalid public key', status=400)

    log.info('adding public key for user: %s', remote_user)
    repo.addkey(remote_user, key)
    return flask.Response(status=200)

#-----------------------------------------------------------------------------
@app.route('/drop/<machine>', methods=['POST'])
def dropkey(machine):
    remote_user = flask.request.environ['REMOTE_USER']

    if not machine:
        return flask.Response('Missing key name', status=400)

    # base64 decode the machine name (must not be unicode)
    machine = base64.urlsafe_b64decode(str(machine)).decode('utf8')

    log.info('removing public key for user: %s', remote_user)
    repo.dropkey(remote_user, machine)
    return flask.Response(status=200)
