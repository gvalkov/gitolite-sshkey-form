#!/usr/bin/env python
# encoding: utf-8

from src import __version__
from setuptools import setup


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
    'Flask>=0.10.1',
    'sh>=1.11',
]

entry_points = {
    'console_scripts': [
        'gitolite_sshkey_form = src.__main__:main'
    ]
}

kw = {
    'name':             'gitolite-sshkey-form',
    'version':          __version__,
    'description':      'Webapp for collecting and managing ssh public keys',
    'long_description': open('README.rst').read(),
    'author':           'Georgi Valkov',
    'author_email':     'georgi.t.valkov@gmail.com',
    'license':          'Revised BSD License',
    'url':              'https://github.com/gvalkov/gitolite-sshkey-form',
    'classifiers':      classifiers,
    'keywords':         'gitolite sshkey',
    'package_dir':      {'gitolite_sshkey_form': 'src'},
    'packages':         ['gitolite_sshkey_form'],
    'entry_points':     entry_points,
    'install_requires': requirements,
    'zip_safe':         False,
    'include_package_data': True,
}

if __name__ == '__main__':
    setup(**kw)
