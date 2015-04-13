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

.. thumbnail::  empty.png
   :width: 22%
   :group: screenshots
   :alt:   Without keys

.. thumbnail::  with-keys.png
   :width: 22%
   :group: screenshots
   :alt:   With keys


Installation
------------

The latest stable version of *web-sshkey-form* can be installed from
pypi_:

.. code-block:: bash

    $ pip install gitolite-sshkey-form

Tailon can also be installed manually:

.. code-block:: bash

    $ git clone git@github.com:gvalkov/tailon.git
    $ cd tailon
    $ git reset --hard HEAD $versiontag
    $ python setup.py install


Quick start
-----------

Tailon is a command-line tool that spawns a http server. It can be
configured entirely from its command-line interface or through a yaml
config file.

To get started with tailon you give it a list of files that you wish
to monitor:

.. code-block:: bash

    $ tailon -f /var/log/nginx/* /var/log/apache/{access,error}.log

If at least one of the specified files is readable by the current user,
tailon will start listening on http://localhost:8080.

Tailon's server-side functionality is documented in its help message::

    $ tailon --help
    Usage: tailon [-c path] [-f path [path ...]] [-h] [-d] [-v] [-b addr:port]
                  [-r path] [-a] [-m [cmd [cmd ...]]]

    Tailon is a webapp for looking at and searching through log files.

    Required arguments:
      -c, --config path               yaml config file
      -f, --files path [path ...]     list of files or file wildcards to expose

    Optional arguments:
      -h, --help                      show this help message and exit
      -d, --debug                     show debug messages
      -v, --version                   show program's version number and exit
      -b, --bind addr:port            listen on the specified address and port
      -r, --relative-root path        web app root path
      -a, --allow-transfers           allow file downloads
      -m, --commands [cmd [cmd ...]]  allowed commands (default: tail grep awk)

    Example config file:
      bind: 0.0.0.0:8080      # address and port to bind on
      allow-transfers: true   # allow file downloads
      relative-root: /tailon  # web app root path (default: '')
      commands: [tail, grep, awk] # allowed commands

      files:
        - '/var/log/messages'
        - '/var/log/nginx/*.log'
        - '/var/log/xorg.[0-10].log'
        - 'cron':
            - '/var/log/cron*'


License
-------

Web-sshkey-helper is released under the terms of the `Revised BSD License`_.

.. _pypi:                  http://pypi.python.org/pypi/web-sshkey-helper
.. _github:                https://github.com/gvalkov/web-sshkey-helper
.. _gitolite:              https://github.com/sitaramc/gitolite
.. _authorization:         http://gitolite.com/gitolite/concepts.html#auth
.. _legacy:                https://github.com/gvalkov/gitolite-sshkey-form/tree/legacy
.. _`Revised BSD License`: https://raw.github.com/gvalkov/tailon/master/LICENSE
