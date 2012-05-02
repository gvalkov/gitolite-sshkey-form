# Gitolite-admin repository to clone (optional)
ADMIN_REPO   = 'git://<changeme>@<changeme>:gitolite-admin'

# Location of ADMIN_REPO working copy. If ADMIN_REPO is set, the webapp will
# clone it into WORKDIR. Adding or removing a key will trigger a push to
# ADMIN_REPO.
#
# If ADMIN_REPO is not set (or set to ''), WORKDIR is just a directory for
# storing keys.
WORKDIR      = '<changeme>' # absolute path

# gitolite-admin branch to which keys should be pushed (optional)
BRANCH       = 'master'

# author/email to use when adding keys to gitolite-admin
AUTHOR_NAME  = 'Gitolite Publickey Form'
AUTHOR_EMAIL = '<nobody@localhost>'

# enable/disable the identities functionality (optional
ENABLE_IDENTITIES = True
IDENTITIES_DB = '<changeme>'

# show public key addition/removal log on /log
ENABLE_LOG = True
