Gitolite-sshkey-form
====================

*Gitolite-sshkey-form* is a simple web app that allows users to submit their
ssh public keys directly to gitolite_. While this can simplify public key
distribution, an administrator still has to give users access rights through
``gitolite-admin.conf``.

*Gitolite-sshkey-form* can also link a gitolite alias (eg. *johndoe*) to a git
identity (eg.  *John Doe <jdoe@email>*). This makes it possible to implement
ad-hoc authentication for git repositories, since gitolite is concerned only
with authorization_.


Screenshots
-----------

.. image::  https://github.com/gvalkov/screenshots/raw/master/thumb/websshkey-01.png
   :target: https://github.com/gvalkov/screenshots/raw/master/full/websshkey-01.png
   :alt:    Without any public keys

.. image::  https://github.com/gvalkov/screenshots/raw/master/thumb/websshkey-02.png
   :target: https://github.com/gvalkov/screenshots/raw/master/full/websshkey-02.png
   :alt:    With two public keys

.. image::  https://github.com/gvalkov/screenshots/raw/master/thumb/websshkey-03.png
   :target: https://github.com/gvalkov/screenshots/raw/master/full/websshkey-03.png
   :alt:    Activity log


Simple Authentication
---------------------

The update.authenticate.sh_ hook can be used to authenticate users that
gitolite has authorized. Once a user has associated their alias (eg.
*johndoe*) with an identity (eg. *John Doe <jdoe@email>*) the hook will compare
that identity against the committer field of all commit object that the user is
attempting to push. In pseudo-code::

    identity  = <fetch gitolite-sshkey-form/get-identity/johndoe>
    revisions = <list of revisions that we're trying to push>

    for revision in revisions:
        committer = <get committer for revision>
        if identity is not committer: complain()

If you wish to disable this functionality, set ``ENABLE_IDENTITIES`` to
``False`` in the configuration file. This would remove the ``/set-identity``,
``/get-identity`` paths, as well as the identity text input from the index
view.

Since *gitolite-sshkey-form* needs a ``REMOTE_USER`` to be set by your
application server, you most likely already have a better service
against which commits can be authenticated (some form of centralized
authentication). The described functionality might be useful if your
authentication backend does not contain all the necessary information
(full name, email) or in cases where it is easier to manage your git
identities separately.


Setup
-----

In the following setup, *gitolite-sshkey-form* will run as the
``gitolite-sshkey-form`` user. This user will have RW access to the
``gitolite-admin`` repository. The webapp and all its dependencies will be
installed in a virtual environment in the user's home directory.


1. Create and become user ``gitolite-sshkey-form``::

    $ sudo useradd -r -m -b /var/lib/ -s /bin/bash -- gitolite-sshkey-form
    $ sudo -u gitolite-sshkey-form -i

2. Create a ssh keypair with an empty passphrase::

    $ ssh-keygen -q -N ''

3. Add the ssh key fingerprint of your gitolite server to ``~/ssh/.known_hosts``::

    # simply accept the fingerprint (no need to login)
    $ ssh gitolite@git.yourdomain.com

4. Give the ``gitolite-sshkey-form`` user access to the gitolite-admin repo::

    # copy .ssh/id_rsa.pub to gitolite-admin/keydir/gitolite-sshkey-form.pub

    # edit gitolite-admin/conf/gitolite.conf

    # give gitolite-sshkey-form RW+ access to the gitolite-admin repo
    # repo    gitolite-admin
    #         RW+ = [... list of users ...] gitolite-sshkey-form

    # once you have pushed your changes to gitolite, verify
    # gitolite-sshkey-form's permissions

    $ ssh gitolite@git.yourdomain.com info | grep gitolite-admin
        R   W     gitolite-admin

5. Create a virtual environment::

    $ virtualenv --no-site-packages ~/venv

6. Install *gitolite-sshkey-form* from pypi (stable version) or github (development)::

    $ ~/venv/bin/pip install gitolite-sshkey-form # stable
    $ ~/venv/bin/pip install git+git://github.com/gvalkov/gitolite-sshkey-form # development

7. Configure gitolite-sshkey-form::

    # download the annotated config file
    $ wget https://raw.github.com/gvalkov/gitolite-sshkey-form/blob/HEAD/etc/config.py

    # and modify according to fit your environment
    $ editor config.py

8. Configure application server (apache + mod_wsgi)::

    # download example wsgi file
    $ wget https://raw.github.com/gvalkov/gitolite-sshkey-form/HEAD/etc/websshkey.wsgi
    $ editor websshkey.py

    # set the path to the config file:
    # environ['WEBSSHKEY_HELPER_CONFIG'] = '/var/lib/gitolite-sshkey-form/config.py'

    # set the path to the bin/activate_this.py file in your virtual environment
    # activate_py = '/var/lib/gitolite-sshkey-form/venv/bin/activate_this.py'

    $ wget https://raw.github.com/gvalkov/gitolite-sshkey-form/HEAD/etc/httpd.conf

The httpd.conf_ file contains an example virtual host configuration running
with mod_wsgi_. You would most certainly need to configure some sort of
authentication (anything that sets a REMOTE_USER).


Setup - Simple Authentication
-----------------------------

1. Enable gitolite update hook chaining::

    $ cd /path/to/gitolite/hooks/common

    $ cp update.secondary.sample update.secondary
    $ chmod +x update.secondary

    $ mkdir update.secondary.d
    $ sudo -u gitolite gl-setup

Gitolite will add symbolic links to ``update.secondary.d`` and
``update.secondary`` in the hooks directory of every repository that it
oversees.

2. Copy the update.authenticate.sh_ script to ``./update.secondary.d``::

    $ wget -P ./update.secondary.d/ http://raw.github.com/gvalkov/gitolite-sshkey-form/blob/master/etc/update.authenticate.sh

    # set 'get_identity_url' in update.authentication.sh
    $ editor ./update.secondary.d/update.authentication.sh


Development
-----------

**Files of potential interest:**

 * views.py_ - all functionality ends up being used here
 * code.js_ - javascript (use sparingly)
 * style.css_ - main stylesheet

**Random notes:**

 * Use the test-run.py_ script to run locally (it also sets a
   ``REMOTE_USER`` for you, since nearly all handlers rely on that being set)

 * The styling of the app is intertwined between the main stylesheet_ and
   the `jquery-ui css`_.

**Tests:**

For testing, *gitolite-sshkey-form* uses the excellent py.test_ framework.
To install testing dependencies and run all tests::

    $ pip install py.test
    $ py.test tests

To run individual tests::

    $ py.test tests/test_$name.py

** Todo **

 * Setting up *gitolite-sshkey-form* is currently overkill for most
   small teams that just want to quickly gather keys. A standalone
   script that serves the webapp and works without an authentication
   backend (everybody can select whatever alias they choose) would be
   nice.

 * The templates and css ended up being a real mess. I suppose they're
   in need of some attention (I'm not really a web developer of any
   kind).

 * Better loading/working indicator.



License
-------
*Gitolite-sshkey-form* is released under the terms of the `New BSD License`_.


.. _gitolite:        http://github.com/sitaramc/gitolite
.. _authorization:   http://sitaramc.github.com/gitolite/auth.html
.. _update.authenticate.sh: http://github.com/gvalkov/gitolite-sshkey-form/blob/master/etc/update.authenticate.sh
.. _httpd.conf:      http://github.com/gvalkov/gitolite-sshkey-form/blob/master/etc/httpd.conf
.. _views.py:        http://github.com/gvalkov/gitolite-sshkey-form/blob/master/gitolite_sshkey_form/views.py
.. _code.js:         http://github.com/gvalkov/gitolite-sshkey-form/blob/master/gitolite_sshkey_form/static/js/code.js
.. _style.css:       http://github.com/gvalkov/gitolite-sshkey-form/blob/master/gitolite_sshkey_form/static/css/style.css
.. _stylesheet:      http://github.com/gvalkov/gitolite-sshkey-form/blob/master/gitolite_sshkey_form/static/css/style.css
.. _jquery-ui css:   http://github.com/gvalkov/gitolite-sshkey-form/blob/master/gitolite_sshkey_form/static/css/custom-theme/jquery-ui-1.8.16.custom.css
.. _test-run.py:     http://github.com/gvalkov/gitolite-sshkey-form/blob/master/gitolite_sshkey_form/test-run.py
.. _py.test:         http://pytest.org/latest/
.. _mod_wsgi:        http://code.google.com/p/modwsgi/
.. _NEW BSD License: https://raw.github.com/gvalkov/gitolite-sshkey-form/master/LICENSE
