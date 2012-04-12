#!/usr/bin/env python
# encoding: utf-8


from os.path import basename, join as pjoin
from util import nextinseq, splitkey, joinkey


class Gitolite(object):
    keydir = 'keydir'
    commit_msg_add = 'Added public key: user "%s", fn "%s"'
    commit_msg_del = 'Removed public key: user "%s", fn "%s"'

    def __init__(self, gitadm, logger):
        self.gitadm = gitadm
        self.logger = logger

    def listkeys(self, user, namesonly=False):
        ''' Yield all key names stored in gitolite for the given user.

            keydir/joe@{1..2}.pub -> [('joe', 1, <data>), ('joe', 2, ..)]
        '''
        tree = self.gitadm.tree(self.keydir)

        for key in tree.traverse():
            act_user, machine = splitkey(key.name)

            if act_user == user:
                yield act_user, machine, None if namesonly else key.data_stream.read()

    def addkey(self, user, data):
        nums = [i[1] for i in self.listkeys(user, True)]
        next = nextinseq(nums)

        fn = pjoin(self.keydir, joinkey(user, next))

        try:
            self.gitadm.pull()
            self.gitadm.reset()
            self.gitadm.write(fn, data)
            self.gitadm.add(fn)
            msg = self.commit_msg_add % (user, fn)
            self.gitadm.commit(msg)
            self.gitadm.push()

            self.logger.info(msg)
        except:
            raise
            try: self.gitadm.rm(fn)
            except: pass

    def dropkey(self, user, machine):
        if machine == 'None': machine = None # @bug

        fn = pjoin(self.keydir, joinkey(user, machine))

        try:
            self.gitadm.pull()
            self.gitadm.reset()
            self.gitadm.rm(fn)
            msg = self.commit_msg_add % (user, fn)
            self.gitadm.commit(self.commit_msg_del % (user, fn))
            self.gitadm.push()

            self.logger.info(msg)
        except:
            raise

    def _keypath(self, name, machine):
        ''' return the absolute path to the user's public key '''

        return pjoin(self.gitadm.repo.working_dir,
                     self.keydir,
                     joinkey(name, machine))

