Introduction
============

*Gitolite-sshkey-form* is a webapp for collecting and managing SSH
public keys. Keys are stored in a directory or committed and pushed
directly to gitolite_.

*Gitolite-sshkey-form* can also link a gitolite alias (eg. *johndoe*)
to a git identity (eg. *John Doe <jdoe@email>*). This makes it
possible to implement ad-hoc authentication for git repositories, as
gitolite is concerned only with authorization_.I

While this tool can simplify public key collection, an administrator
still has to assign access rights through ``gitolite-admin.conf``.


Screenshots
-----------

.. thumbnail::  screenshots/empty.png
   :width: 30%
   :group: screenshots
   :alt:   Without keys

.. thumbnail::  screenshots/with-keys.png
   :width: 30%
   :group: screenshots
   :alt:   With keys


Installation
------------

The latest stable version of *web-sshkey-form* can be installed from
pypi_:

.. code-block:: bash

    $ pip install gitolite-sshkey-form

Work in progress
----------------

License
-------

Web-sshkey-helper is released under the terms of the `Revised BSD License`_.

.. _pypi:                  http://pypi.python.org/pypi/web-sshkey-helper
.. _github:                https://github.com/gvalkov/web-sshkey-helper
.. _gitolite:              https://github.com/sitaramc/gitolite
.. _authorization:         http://gitolite.com/gitolite/concepts.html#auth
.. _legacy:                https://github.com/gvalkov/gitolite-sshkey-form/tree/legacy
.. _`Revised BSD License`: https://raw.github.com/gvalkov/tailon/master/LICENSE
