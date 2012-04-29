#!/usr/bin/env python
# encoding: utf-8

from os.path import abspath, dirname, join as pjoin
from setuptools import setup, find_packages, Command
from gitolite_sshkey_form.version import version

here = abspath(dirname(__file__))

requires = ('flask', 'gitpython')
test_requires = ('pytest', 'mock')

classifiers = [
    'Programming Language :: Python',
    'License :: OSI Approved :: BSD License',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content :: CGI Tools/Libraries',
    'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
    #'Development Status :: 1 - Planning',
    #'Development Status :: 2 - Pre-Alpha',
    #'Development Status :: 3 - Alpha',
    'Development Status :: 4 - Beta',
    #'Development Status :: 5 - Production/Stable',
    #'Development Status :: 6 - Mature',
    #'Development Status :: 7 - Inactive',
]

kw = {
    'name'                 : 'gitolite-sshkey-form',
    'version'              : version(),

    'description'          : 'webapp for submitting ssh public keys directly to gitolite',
    'long_description'     : open(pjoin(here, 'README.rst')).read(),

    'author'               : 'Georgi Valkov',
    'author_email'         : 'georgi.t.valkov@gmail.com',

    'license'              : 'New BSD License',

    'keywords'             : 'gitolite sshkey',
    'classifiers'          : classifiers,

    'url'                  : 'https://github.com/gvalkov/gitolite-sshkey-form',

    'packages'             : find_packages(exclude=['tests']),
    'install_requires'     : requires,

    'tests_require'        : test_requires,
    'cmdclass'             : {},

    'include_package_data' : True,
    'zip_safe'             : False,
}


class PyTest(Command):
    user_options = []
    def initialize_options(self): pass
    def finalize_options(self):   pass
    def run(self):
        from subprocess import call
        errno = call(('py.test', 'tests'))
        raise SystemExit(errno)


kw['cmdclass']['test'] = PyTest
setup(**kw)
