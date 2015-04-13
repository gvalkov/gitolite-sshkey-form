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


License
-------

This project is released under the terms of the `Revised BSD License`_.

.. _gitolite:        https://github.com/sitaramc/gitolite
.. _authorization:   http://gitolite.com/gitolite/concepts.html#auth
.. _legacy:          https://github.com/gvalkov/gitolite-sshkey-form/tree/legacy
.. _Revised BSD License: https://raw.github.com/gvalkov/gitolite-sshkey-form/master/LICENSE


Legacy
------

If you are looking for the Perl/Dancer version of this project, please
have a look at the legacy_ branch.
