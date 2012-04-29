#!/usr/bin/env python
# encoding: utf-8

import flask

from flask import request

from gitolite_sshkey_form.app  import app
from gitolite_sshkey_form.util import iskeyvalid, listkeys64, urlsafe_b64decode
from gitolite_sshkey_form.dir  import Dir
from gitolite_sshkey_form.gitadmin import GitAdmin
from gitolite_sshkey_form.gitolite import Gitolite
from gitolite_sshkey_form.identities import Identities


def repoconnect():
    kw = {
        'workdir' : app.config['WORKDIR'],
        'branch'  : app.config.get('BRANCH', None),
        'repourl' : app.config.get('ADMIN_REPO', None),
        'author_name'  : app.config.get('AUTHOR_NAME', 'Gitolite Publickey Form'),
        'author_email' : app.config.get('AUTHOR_EMAIL', 'nobody@localhost'),
    }

    if kw['repourl']:
        repo = GitAdmin(**kw)
        return Gitolite(repo, app.logger)
    else:
        return Dir(kw['workdir'], app.logger)


@app.before_first_request
def configure():
    # if we're running from test-run.py we would have already set things up
    if not (app.config['TESTING'] and app.config['ADMIN_REPO']):
        app.config.from_envvar('WEBSSHKEY_HELPER_CONFIG')


@app.before_request
def initialize():
    with_idn = app.config['ENABLE_IDENTITIES']

    store      = getattr(flask.g, 'store',      None)
    identities = getattr(flask.g, 'identities', None)

    if not store:
        flask.g.store = repoconnect()

    if with_idn and not identities:
        sql = app.open_resource('schema.sql').read()
        flask.g.identities = Identities(app.config['IDENTITIES_DB'], sql)


@app.route('/')
def index():
    remote_user = request.environ['REMOTE_USER']
    keys = flask.g.store.listkeys(remote_user)

    # base64 encode the machine name
    keys = listkeys64(keys)

    env = {
        'remote_user' : remote_user,
        'sshkeys'     : list(keys),
        'enable_identities' : app.config['ENABLE_IDENTITIES']
    }

    if app.config['ENABLE_IDENTITIES']:
        # this is where you could set the user's identity to a reasonable
        # default (from ldap for example)

        identity = flask.g.identities.get(remote_user)
        env['git_identity'] = identity and identity or ''

    return flask.render_template('index.jinja', **env)


@app.route('/add', methods=['POST'])
def addkey():
    remote_user = request.environ['REMOTE_USER']
    key = request.form.get('key', None)

    if not key:
        return flask.Response('Empty public key', status=400)

    if not iskeyvalid(key):
        return flask.Response('Invalid public key', status=400)

    flask.g.store.addkey(remote_user, key)
    return flask.Response(status=200)


@app.route('/drop/<machine>', methods=['POST'])
def dropkey(machine):
    remote_user = request.environ['REMOTE_USER']

    if not machine:
        return flask.Response('Missing key name', status=400)

    # base64 decode the machine name (must not be unicode)
    machine = urlsafe_b64decode(str(machine))

    flask.g.store.dropkey(remote_user, machine)
    return flask.Response(status=200)


@app.route('/set-identity', methods=['POST'])
def setidentity():
    if not app.config['ENABLE_IDENTITIES']:
        return flask.Response(status=404)

    remote_user = request.environ['REMOTE_USER']
    identity = request.form.get('identity', None)

    if not identity:
        return flask.Response('Zero-lenght identity', status=400)

    flask.g.identities.add(remote_user, identity)

    app.logger.info('Updated identity for user "%s" to "%s"', remote_user, identity)
    return flask.Response(status=200)


@app.route('/get-identity/<alias>', methods=['POST', 'GET'])
def getidentity(alias):
    if not app.config['ENABLE_IDENTITIES']:
        return flask.Response(status=404)

    identity = flask.g.identities.get(alias)

    if not identity:
        return flask.Response('Identity for user %s not found' % alias, status=400)

    return flask.Response(identity, status=200)

