# -*- coding: utf-8; -*-

from __future__ import absolute_import
from __future__ import print_function

import os, re, sys
import shutil
import logging

from pathlib import Path
from abc import ABCMeta, abstractmethod
from sh import Command

from . import utils


#-----------------------------------------------------------------------------
log = logging.getLogger('backends')

#-----------------------------------------------------------------------------
class BackendError(Exception):
    pass

#-----------------------------------------------------------------------------
class Backend(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def listkeys(self, user, namesonly=False):
        '''
        Yield all key names for the given user. Optionally also output
        key contents.

        >>> list(listkeys('joe'), namesonly=True)
        ... [('joe', 1), ('joe', 2)]

        >>> list(listkeys('joe'))
        ... [('joe', 1, <data>), ('joe', 2, <data>)]
        '''
        pass

    @abstractmethod
    def addkey(self, user, data):
        pass

    @abstractmethod
    def dropkey(self, user, machine):
        pass

    @abstractmethod
    def keyexists(self, user, key):
        pass


#-----------------------------------------------------------------------------
class Directory(Backend):
    def __init__(self, workdir):
        self.workdir = workdir = Path(workdir)

        if not workdir.exists():
            workdir.mkdir(parents=True)
        elif not workdir.is_dir():
            raise Exception('%s is not a directory' % workdir)

    def listkeys(self, user, namesonly=False):
        keys = self.workdir.glob('%s@*.pub' % user)
        for key in keys:
            actual_user, machine = utils.splitkey(key.name)

            if actual_user == user:
                data = key.open().read() if not namesonly else None
                yield actual_user, machine, data

    def addkey(self, user, data):
        nums = [i[1] for i in self.listkeys(user, True)]
        nextnum = utils.nextinseq(nums)

        keyname = utils.joinkey(user, nextnum)
        with (self.workdir / keyname).open('wb') as fh:
            fh.write(data.encode('utf8'))
            return fh.name

    def dropkey(self, user, machine):
        path = self.workdir / utils.joinkey(user, machine)
        path.unlink()

    def keyexists(self, user, key):
        return any(data == key for _, _, data in self.listkeys(user))


#-----------------------------------------------------------------------------
class Gitolite(Backend):
    commit_msg_add = 'Added public key: user "{}", fn "{}"'
    commit_msg_del = 'Removed public key: user "{}", fn "{}"'

    def __init__(self, workdir, url, author, gitcmd='git'):
        self.workdir = workdir
        self.author = author
        self.url = url
        self.git = Command(gitcmd)
        self.git = self.setup()

    def setup(self):
        if not (self.workdir / '.git').is_dir():
            shutil.rmtree(str(self.workdir))
            self.git('clone', self.url, str(self.workdir))
        else:
            remote_url = self.git('remote', 'show', 'origin', '-n', _cwd=str(self.workdir))
            remote_url = re.findall('^\s*Fetch URL: (.*)$', str(remote_url), re.MULTILINE)[0]

            if remote_url != self.url:
                log.info('removing workdir: %s', self.workdir)
                shutil.rmtree(str(self.workdir))
                self.git('clone', self.url, str(self.workdir))

        if not (self.workdir / 'keydir').is_dir():
            raise BackendError('%s does not exist (is this a gitolite repository?)' % self.workdir)

        return self.git.bake(_cwd=str(self.workdir))

    def listkeys(self, user, namesonly=False):
        files = self.git('ls-files', 'keydir').splitlines()
        files = (self.workdir/i for i in files if i.endswith('.pub'))

        for key in files:
            actual_user, machine = utils.splitkey(key.name)

            if actual_user == user:
                data = key.open().read() if not namesonly else None
                yield actual_user, machine, data

    def addkey(self, user, data):
        nums = [i[1] for i in self.listkeys(user, True)]
        nextnum = utils.nextinseq(nums)
        keyname = utils.joinkey(user, nextnum)
        relpath = 'keydir/%s' % keyname
        path = self.workdir / relpath

        self.git('fetch', 'origin')
        self.git('reset', '--hard', 'origin/HEAD')

        with path.open('wb') as fh:
            fh.write(data.encode('utf8'))

        self.git('add', relpath)
        self.git('commit', relpath,
                 '--author', self.author,
                 '--message', self.commit_msg_add.format(user, relpath))
        self.git('push', 'origin', 'HEAD')

        return path

    def dropkey(self, user, machine):
        relpath = 'keydir/%s' % utils.joinkey(user, machine)
        self.git('fetch', 'origin',)
        self.git('reset', '--hard', 'origin/HEAD')
        self.git('rm', relpath)
        self.git('commit', relpath,
                 '--author', self.author,
                 '--message', self.commit_msg_del.format(user, relpath))
        self.git('push', 'origin', 'HEAD')

    def keyexists(self, user, key):
        return any(data == key for _, _, data in self.listkeys(user))
