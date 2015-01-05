This is a work in progress. If you are looking for the Python/Flask
version of this project, look at the legacy_ branch.

Introduction
============

*Gitolite-sshkey-form* is a webapp for collecting and managing SSH
public keys.  Keys are stored in a directory or committed and pushed
directly to gitolite_.

*Gitolite-sshkey-form* can also link a gitolite alias (eg. *johndoe*)
to a git identity (eg.  *John Doe <jdoe@email>*). This makes it
possible to implement ad-hoc authentication for git repositories, as
gitolite is concerned only with authorization_.

While this tool can simplify public key distribution, an administrator
still has to assign access rights through ``gitolite-admin.conf``.

Screenshots
-----------

.. image::  https://github.com/gvalkov/gitolite-sshkey-form/raw/master/.screenshots/empty-thumb.png
   :target: https://github.com/gvalkov/gitolite-sshkey-form/raw/master/.screenshots/empty.png
   :alt:    Without public keys

.. image::  https://github.com/gvalkov/gitolite-sshkey-form/raw/master/.screenshots/with-keys-thumb.png
   :target: https://github.com/gvalkov/gitolite-sshkey-form/raw/master/.screenshots/with-keys.png
   :alt:    With public keys

Usage
-----

1. Follow `these instructions <http://search.cpan.org/~miyagawa/App-cpanminus-1.7023/lib/App/cpanminus.pm#INSTALLATION>`_ to install cpanminus_.

2. Clone and install dependencies:

   .. code-block:: bash

       $ git clone https://github.com/gvalkov/gitolite-sshkey-form
       $ cd gitolite-sshkey-form
       $ cpanm --installdeps .

3. Edit the ``config.yml`` file to suit your needs.

4. Run with ``plackup``:

   .. code-block:: bash

       $ plackup --host 127.0.0.1 --port 8080 bin/app.psgi

   For more deployment options, refer to ``plackup --help`` and the
   Dancer2_ documentation.

License
-------

*Gitolite-sshkey-form* is released under the terms of the `Revised BSD License`_.

.. _gitolite:        https://github.com/sitaramc/gitolite
.. _authorization:   https://sitaramc.github.com/gitolite/auth.html
.. _legacy:          https://github.com/gvalkov/gitolite-sshkey-form/tree/legacy
.. _cpanminus:       http://search.cpan.org/~miyagawa/App-cpanminus-1.7023
.. _Dancer2:         http://search.cpan.org/~sukria/Dancer2-0.01/lib/Dancer2/Deployment.pod

.. _Revised BSD License: https://raw.github.com/gvalkov/gitolite-sshkey-form/master/LICENSE
