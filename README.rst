Gitolite-sshkey-form
====================

*Gitolite-sshkey-form* is a simple web app that allows users to submit their
ssh public keys directly to [gitolite][gitolite]. While this can simplify
public key distribution, an administrator still has to give users access rights
through `gitolite-admin.conf`.

Gitolite-sshkey-form can also link a gitolite alias (eg. `johndoe`) to a git
identity (eg.  `John Doe <jdoe@email>`). This makes it possible to implement
ad-hoc authentication for git repositories, since gitolite is concerned only
with [authorization][gitolite-auth].


Screenshots
-----------

<div style='float:left'>
<a href='https://github.com/gvalkov/screenshots/raw/master/full/websshkey-01.png'>
<img align='top' src='https://github.com/gvalkov/screenshots/raw/master/thumb/websshkey-01.png' alt='Without any public keys' />
</a>
</div>

<div style='float:left;'>
<a href='https://github.com/gvalkov/screenshots/raw/master/full/websshkey-02.png'>
<img align='top' src='https://github.com/gvalkov/screenshots/raw/master/thumb/websshkey-02.png' alt='With two public keys' />
</a>
</div>


Simple Authentication
---------------------

The [update.authenticate.sh][update] hook can be used to authenticate users
that gitolite has authorized. Once a user has associated their alias (eg.
`johndoe`) with an identity (eg. `John Doe <jdoe@email>`) the hook will compare
that identity against the committer field of all commit object that the user is
attempting to push. In pseudo-code:

        identity  = <fetch gitolite-sshkey-form/get-identity/johndoe>
        revisions = <list revisions that we're trying to push>

        for revision in revisions:
            committer = <get committer for revision>
            if identity is not committer: complain()

If you wish to disable this functionality, set `ENABLE_IDENTITIES` to `False`
in the configuration file. This would remove the `/set-identity`, `/get-identity`
paths, as well as the identity text input from the index view.

Since gitolite-sshkey-form needs a `REMOTE_USER` to be set by your application
server, you most likely already have a better service against which to
authenticate commits (centralized authentication). The described functionality
might be useful if your autentication backend does not contain all the
necessary information (full name, email) or in cases where it is easier to
manage your git identity seperately.


Setup
-----

In the described setup, *gitolite-sshkey-form* will run as the
`gitolite-sshkey-form` user. This user will contain 


1. Create webapp user 

        $ sudo useradd -r -m -b /var/lib/ -s /bin/bash -- gitolite-sshkey-form

2. Create ssh keypair as user `gitolite-sshkey-form` 

        $ sudo -u gitolite-sshkey-form -i
        $ ssh-keygen -q -N ''

3. Add the ssh key fingerprint of your gitolite server to ~/ssh/.known\_hosts

        # simply accept the fingerprint (no need to login)
        $ ssh gitolite@git.yourdomain.com

4. Give the web-sskey-helper user access to the gitolite admin repo

        # copy /var/lib/gitolite-sshkey-form/.ssh/id_rsa.pub to gitolite-admin/keydir/gitolite-sshkey-form.pub

        # edit gitolite-admin/conf/gitolite.conf

        # give gitolite-sshkey-form RW+ access to the gitolite-admin repo
        # repo    gitolite-admin
        #         RW+ = [... list of users ...] gitolite-sshkey-form

        # once you have pushed your changes to gitolite, verify gitolite-sshkey-form's permissions
        $ ssh gitolite@git.yourdomain.com info | grep gitolite-admin
          R   W     gitolite-admin

5. Checkout/Extract the latest stable version

        $ curl -L http://github.com/gvalkov/gitolite-sshkey-form/tarball/master | tar --xform 's,[^/]*,src,' -xzv  
        @todo: alignment problem when using line continuations

6. Install in a virtual environment

        $ virtualenv --no-site-packages ~/env
        $ cd src && ~/env/bin/python setup.py install

6. Configure gitolite-sshkey-form

        $ cp src/etc/config.py ./config.py
        $ cp src/etc/websshkey.wsgi ./websshkey.wsgi

        $ editor config.py 

        # set the path to the config file:
        # environ['WEBSSHKEY_HELPER_CONFIG'] = '/var/lib/gitolite-sshkey-form/config.py'
        $ editor websshkey.wsgi

7. Configure application server (apache + mod\_wsgi)

    The [httpd.conf][httpd] file contains an example virtual host configuration
    running with mod_wsgi.


Setup - Simple Authentication
=============================

1. Enable gitolite update hook chaining

        $ cd /path/to/gitolite/hooks/common

        $ cp update.secondary.sample update.secondary
        $ chmod +x update.secondary

        $ mkdir update.secondary.d
        $ sudo -u gitolite gl-setup

    Gitolite will add symbolic links to `update.secondary.d` and
    `update.secondary` in the hooks directory of every repository that it
    oversees.

2. Copy update.authentication script to ./update.secondary.d

        $ cp /var/lib/gitolite-sshkey-form/src/etc/update.authentication.sh  ./update.secondary.d/

        # set 'get_identity_url' in update.authentication.sh
        $ editor ./update.secondary.d/update.authentication.sh


Development
===========

__Files of potential interest:__

 * [views.py][views] - all functionality ends up being used here
 * [code.js][codejs] - javascript (use sparingly)
 * [style.css][css] - main stylesheet

__Random notes:__

 * Use the [test-run.py][testrun] script to run locally (it also set a
   `REMOTE_USER` for you, since nearly all handlers rely on that being set)

 * The styling of the app is intertwined between the main [stylesheet][css] and
   the [jquery-ui css][cssjq]. 

__Tests:__
 
For testing, gitolite-sshkey-form uses the excellent [attest][attest] framework.
Tests are organized as modules under `/tests`. To run all tests, as well as
resolve any testing dependencies, run:
        
        $ python setup.py test  # or
        $ python tests/__init__.py

To run individual tests:

        $ python tests/test_$name.py
 
[gitolite]:      http://github.com/sitaramc/gitolite
[gitolite-auth]: http://sitaramc.github.com/gitolite/doc/authentication-vs-authorisation.html
[update]:        http://github.com/gvalkov/gitolite-sshkey-form/blob/master/etc/update.authenticate.sh
[httpd]:         http://github.com/gvalkov/gitolite-sshkey-form/blob/master/etc/httpd.conf
[views]:         http://github.com/gvalkov/gitolite-sshkey-form/blob/master/websshkey/views.py
[codejs]:        http://github.com/gvalkov/gitolite-sshkey-form/blob/master/websshkey/static/js/code.js
[vendorjs]:      http://github.com/gvalkov/gitolite-sshkey-form/blob/master/websshkey/static/js/code.js
[css]:           http://github.com/gvalkov/gitolite-sshkey-form/blob/master/websshkey/static/css/style.css
[cssjq]:         http://github.com/gvalkov/gitolite-sshkey-form/blob/master/websshkey/static/css/custom-theme/jquery-ui-1.8.16.custom.css
[testrun]:       http://github.com/gvalkov/gitolite-sshkey-form/blob/master/websshkey/test-run.py
[attest]:        http://github.com/dag/attest
