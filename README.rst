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

.. image::  https://github.com/gvalkov/screenshots/raw/master/thumb/websshkey-01.png
   :target: https://github.com/gvalkov/screenshots/raw/master/full/websshkey-01.png
   :alt:    Without any public keys

.. image::  https://github.com/gvalkov/screenshots/raw/master/thumb/websshkey-02.png
   :target: https://github.com/gvalkov/screenshots/raw/master/full/websshkey-02.png
   :alt:    With two public keys

License
-------

*Gitolite-sshkey-form* is released under the terms of the `Revised BSD License`_.

.. _gitolite:        https://github.com/sitaramc/gitolite
.. _authorization:   https://sitaramc.github.com/gitolite/auth.html
.. _legacy:          https://github.com/gvalkov/gitolite-sshkey-form/tree/master

.. _Revised BSD License: https://raw.github.com/gvalkov/gitolite-sshkey-form/master/LICENSE
