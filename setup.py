#!/usr/bin/env python
# encoding: utf-8

from websshkey import __version__
from os.path import abspath, dirname, join
from setuptools import setup


here = abspath(dirname(__file__))

classifiers = [
    'Programming Language :: Python',
    'License :: OSI Approved :: BSD License',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content :: CGI Tools/Libraries',
    'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Development Status :: 5 - Production/Stable',
]

requirements = [
    'Flask==0.10.1',
]

kw = {
    'name':             'gitolite-sshkey-form',
    'version':          __version__,
    'description':      'Webapp for collecting and managing public keys',
    'long_description': open(join(here, 'README.rst')).read(),
    'author':           'Georgi Valkov',
    'author_email':     'georgi.t.valkov@gmail.com',
    'license':          'Revised BSD License',
    'url':              'https://github.com/gvalkov/gitolite-sshkey-form',
    'keywords':         'gitolite sshkey',
    'packages':         ['websshkey'],
    'classifiers':      classifiers,
    'install_requires': requirements,
    'include_package_data': True,
    'zip_safe': False,
    'entry_points': {
        'console_scripts': [
            'websshkey = websshkey.main:main'
        ]
    },
}

if __name__ == '__main__':
    setup(**kw)
