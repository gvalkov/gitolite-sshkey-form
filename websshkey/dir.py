#!/usr/bin/env python
# encoding: utf-8


from glob import glob
from os import unlink, makedirs
from os.path import basename, join as pjoin, exists, isdir
from util import nextinseq, splitkey, joinkey


class Dir(object):
    commit_msg_add = 'Added public key: user "%s", fn "%s"'
    commit_msg_del = 'Removed public key: user "%s", fn "%s"'

    def __init__(self, keydir, logger):

        if not exists(keydir):
            makedirs(keydir)
        elif not isdir(keydir):
            raise Exception('%s is not a directory' % keydir)

        self.keydir = keydir
        self.logger = logger

    def listkeys(self, user, namesonly=False):
        ''' Yield all key names stored in the keydir for the given user.

            joe@{1..2}.pub -> [('joe', 1, <data>), ('joe', 2, ..)]
        '''

        for key in glob('%s/%s@*' % (self.keydir, user)):
            act_user, machine = splitkey(basename(key))

            if act_user == user:
                yield act_user, machine, None if namesonly else open(key).read()

    def addkey(self, user, data):
        nums = [i[1] for i in self.listkeys(user, True)]
        next = nextinseq(nums)

        fn = pjoin(self.keydir, joinkey(user, next))

        with open(fn, 'w') as fh:
            fh.write(data)

        msg = self.commit_msg_add % (user, fn)
        self.logger.info(msg)

    def dropkey(self, user, machine):
        if machine == 'None': machine = None # @bug

        fn = pjoin(self.keydir, joinkey(user, machine))

        unlink(fn)
        msg = self.commit_msg_del % (user, fn)
        self.logger.info(msg)

    def _keypath(self, name, machine):
        return pjoin( self.keydir, joinkey(name, machine))

