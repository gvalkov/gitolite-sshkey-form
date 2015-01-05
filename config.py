# The gitolite-admin repository to clone (optional).
#ADMIN_REPO = '<changeme>'

# Depending on the value of ADMIN_REPO, WORKDIR is one one of:
# 1) If ADMIN_REPO is set, WORKDIR is the checkout location (the
#    working copy) of ADMIN_REPO. When a key is added or removed, the
#    webapp will commit and push to ADMIN_REPO.
# 2) If ADMIN_REPO is not set (or set to ''), WORKDIR will be treated
#    as a plain directory in which to store public keys.
WORKDIR = '/tmp/outdir'

# The gitolite-admin branch to which keys should be pushed (optional).
BRANCH = 'master'

# Author/email to use when adding keys to gitolite-admin.
AUTHOR_NAME  = 'Gitolite Public Key Form'
AUTHOR_EMAIL = '<nobody@localhost>'
