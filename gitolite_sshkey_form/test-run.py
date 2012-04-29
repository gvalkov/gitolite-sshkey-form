#!/usr/bin/env python
# encoding: utf-8

from os import environ
from shutil import rmtree
from os.path import abspath, dirname,join

from tests import util
from gitolite_sshkey_form.app import app

config = join(abspath(dirname(__file__)), '../etc/test-config.py')
environ['WEBSSHKEY_HELPER_CONFIG'] = config

repourl, aliases = util.createGitoliteGitRepo(2, 2, True)
print('created temporary gitolite repo in {}'.format(repourl))

app.config.from_envvar('WEBSSHKEY_HELPER_CONFIG')
app.config['TESTING'] = True
app.config['ADMIN_REPO'] = repourl


def TestMiddleware(app):
    def inner(environ, start_response):
        environ['REMOTE_USER'] = 'johndoe'
        return app(environ, start_response)
    return inner

try:
    app.wsgi_app = TestMiddleware(app.wsgi_app)
    app.run(debug=True)
finally:
    print('removing temporary gitolite repo {}'.format(repourl))
    rmtree(repourl)
    print('removing gitolite working dir {}'.format(app.config['WORKDIR']))
    rmtree(app.config['WORKDIR'])

