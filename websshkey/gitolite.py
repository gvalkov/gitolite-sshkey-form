#!/usr/bin/env python
# encoding: utf-8


from os.path import basename, join as pjoin
from util import nextinseq


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
            act_user, machine = self._splitkey(key.name)

            if act_user == user:
                yield act_user, machine, None if namesonly else key.data_stream.read()

    def addkey(self, user, data):
        nums = [i[1] for i in self.listkeys(user, True)]
        next = nextinseq(nums)

        fn = pjoin(self.keydir, self._joinkey(user, next))

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

        fn = pjoin(self.keydir, self._joinkey(user, machine))

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

    def _splitkey(self, name):
        ''' 'joe@1.pub'  -> 'joe', '1'
            'joe@pc.pub' -> 'joe', 'pc'
            'joe.pub'    -> 'joe', None
        '''

        name = basename(name)
        name = name.rstrip('.pub').split('@')

        if len(name) == 1:
            return name[0], None
        elif type(name[1]) :
            return name[0], name[1]

    def _joinkey(self, name, machine):
        ''' 'joe', int(1) -> 'joe@1.pub'
            'joe', None   -> 'joe.pub'
        '''

        if machine is None: return name + '.pub'
        else:               return '%s@%s.pub' % (name, machine)


    def _keypath(self, name, machine):
        ''' return the absolute path to the user's public key '''

        return pjoin(self.gitadm.repo.working_dir,
                     self.keydir,
                     self._joinkey(name, machine))

