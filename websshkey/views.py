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
def configure():
    #-------------------------------------------------------------------------
    # Read config from environment
    #-------------------------------------------------------------------------
    config = app.config.get
    author_name       = config('AUTHOR_NAME', 'Gitolite Publickey Form')
    author_email      = config('AUTHOR_EMAIL' 'nobody@localhost')
    admin_repo_url    = config('ADMIN_REPO', '')
    admin_repo_branch = config('BRANCH', 'master')
    workdir           = config('WORKDIR')

    if not workdir:
        print('The WORKDIR config key is not set.', file=sys.stderr)
        sys.exit(1)

    #-------------------------------------------------------------------------
    if admin_repo_url:
        author = '%s <%s>' % (author_name, author_email)
        repo = backends.Gitolite(workdir, admin_repo_url, author)
    else:
        repo = backends.Directory(workdir)

    del config
    globals().update(locals())

@app.before_first_request
def flask_configure():
    try:
        configure()
    except SystemExit:
        raise flask.abort(500)

#-----------------------------------------------------------------------------
@app.before_request
def check_remote_user():
    user = flask.request.environ['REMOTE_USER']
    if user is None:
        raise flask.abort(401)

#-----------------------------------------------------------------------------
@app.route('/', methods=['GET'])
def index():
    user = flask.request.environ['REMOTE_USER']
    keys = repo.listkeys(user)
    keys = utils.listkeys64(keys)

    ctx = {
        'user': user,
        'sshkeys': list(keys),
        'enable_identities': app.config.get('ENABLE_IDENTITIES')
    }

    return flask.render_template('index.jinja', **ctx)

#-----------------------------------------------------------------------------
@app.route('/add', methods=['POST'])
def addkey():
    user = flask.request.environ['REMOTE_USER']
    key = flask.request.form.get('data')

    if not key:
        return flask.Response('Empty public key', status=400)

    if not utils.iskeyvalid(key):
        return flask.Response('Invalid public key', status=400)

    if repo.keyexists(user, key):
        return flask.Response(status=200)

    log.info('adding public key for user: %s', user)
    repo.addkey(user, key)
    return flask.Response(status=200)

#-----------------------------------------------------------------------------
@app.route('/drop/<machine>', methods=['POST'])
def dropkey(machine):
    user = flask.request.environ['REMOTE_USER']

    if not machine:
        return flask.Response('Missing key name', status=400)

    # Base64 decode the machine name (must not be unicode).
    machine = base64.urlsafe_b64decode(str(machine)).decode('utf8')

    log.info('removing public key for user: %s', user)
    repo.dropkey(user, machine)
    return flask.Response(status=200)
