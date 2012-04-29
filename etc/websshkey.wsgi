# vim: ft=python

from os import environ

# path to config file
environ['WEBSSHKEY_HELPER_CONFIG'] = '/var/lib/gitolite-sshkey-form/config.py'


activate_py = '/var/lib/gitolite-sshkey-form/venv/bin/activate_this.py'
execfile(activate_py, dict(__file__=activate_py))

# or

#import site
#site.addsitedir("/var/lib/web-sshkey-helper/env/lib/pythonX.X/site-packages")


from gitolite_sshkey_.app import app as application
