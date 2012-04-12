# Gitolite-admin repository to clone (optional)
ADMIN_REPO   = 'gitolite@localhost:gitolite-admin'

# Location of ADMIN_REPO working copy. If ADMIN_REPO is set, the webapp will
# clone it into WORKDIR. Adding or removing a key will trigger a push to
# ADMIN_REPO.
#
# If ADMIN_REPO is not set (or set to ''), WORKDIR is just a directory for
# storing keys.
WORKDIR      = '/tmp/websshkey-workdir'

# gitolite-admin branch to which keys should be pushed (optional)
BRANCH       = 'master'

# author/email to use when adding keys to gitolite-admin (optional)
AUTHOR_NAME  = 'Gitolite Form'
AUTHOR_EMAIL = '<nobody@localhost>'

# enable/disable the identity functionality
ENABLE_IDENTITIES = True
IDENTITIES_DB = '/tmp/websshkey-identities.sql'
