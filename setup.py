#!/usr/bin/env python
# encoding: utf-8

import os

from os.path import abspath, dirname
from setuptools import setup, find_packages

from websshkey.version import version

here = abspath(dirname(__file__))

requires = ('flask', 'gitpython')
test_requires = ('attest', 'flask-attest', 'mock')

classifiers = [
    'Programming Language :: Python',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content :: CGI Tools/Libraries',
    'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
]

kw = {
    'name'                 : 'web-sshkey-helper',
    'version'              : version(),

    'description'          : 'SSH key managent for gitolite',
    'long_description'     : 'To be defined',

    'author'               : 'Georgi Valkov',
    'author_email'         : 'georgi.t.valkov@gmail.com',

    'license'              : 'New BSD License',

    'keywords'             : 'gitolite sshkey',
    'classifiers'          : classifiers,

    'url'                  : 'https://github.com/gvalkov/gitolite-sshkey-form',

    'packages'             : find_packages(exclude=['tests']),
    'install_requires'     : requires,

    'test_requires'        : test_requires,
    'test_loader'          : 'attest:auto_reporter.test_loader',
    'test_suite'           : 'tests.all',

    'include_package_data' : True,
    'zip_safe'             : False,
}

setup(**kw)
