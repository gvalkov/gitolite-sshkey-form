# -*- coding: utf-8; -*-

from pathlib import Path
from . import utils


class Backend:
    pass

class Directory(Backend):
    def __init__(self, workdir):
        self.workdir = workdir = Path(workdir)

        if not workdir.exists():
            workdir.mkdir(parents=True)
        elif not workdir.is_dir():
            raise Exception('%s is not a directory' % workdir)

    def listkeys(self, user, namesonly=False):
        '''
        Yield all key names stored in the keydir for the given user.
        For example::

          joe@{1..2}.pub -> [('joe', 1, <data>), ('joe', 2, <data>)]
        '''

        keys = self.workdir.glob('%s@*.pub' % user)
        for key in keys:
            actual_user, machine = utils.splitkey(key.name)

            if actual_user == user:
                data = key.open().read() if not namesonly else None
                yield actual_user, machine, data

    def addkey(self, user, data):
        nums = [i[1] for i in self.listkeys(user, True)]
        nextnum = utils.nextinseq(*nums)

        keyname = utils.joinkey(user, nextnum)
        with (self.workdir / keyname).open('w') as fh:
            fh.write(data)
            return fh.name

    def dropkey(self, user, machine):
        path = self.workdir / utils.joinkey(user, machine)
        path.unlink()

    def keyexists(self, user, key):
        return any(data == key for _, _, data in self.listkeys(user))
