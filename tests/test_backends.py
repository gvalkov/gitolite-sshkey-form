# -*- coding: utf-8; -*-

import os
import pytest
from sh import mkdir, touch, git

from websshkey.backends import Directory, Gitolite
from utils import sshkeygen


#-----------------------------------------------------------------------------
@pytest.yield_fixture
def dirrepo(tmpdir):
    repo = Directory(str(tmpdir))
    yield repo

@pytest.yield_fixture
def gitrepo(tmpdir):
    git('init', '--bare', 'bare',   _cwd=str(tmpdir))
    git('clone', 'bare', 'workdir', _cwd=str(tmpdir))

    mkdir('-p', '%s/workdir/keydir' % tmpdir)
    touch('%s/workdir/keydir/.keep' % tmpdir)

    git('add', 'keydir/.keep', _cwd='%s/workdir' % tmpdir)
    git('commit', '-m', '', '--allow-empty-message', 'keydir/.keep', _cwd='%s/workdir' % tmpdir)
    git('push', 'origin', 'HEAD')

    repo = Gitolite('%s/workdir' % tmpdir)
    yield repo


#-----------------------------------------------------------------------------
def test_create(tmpdir):
    dirrepo = Directory(str(tmpdir))

    with pytest.raises(Exception):
        Directory('/etc/fstab')

def test_dir_basic(dirrepo):
    joe1 = sshkeygen(dirrepo.workdir / 'joe@1')
    joe2 = sshkeygen(dirrepo.workdir / 'joe@2')

    #-------------------------------------------------------------------------
    assert dirrepo.keyexists('joe', joe1)
    assert not dirrepo.keyexists('joe', 'asdf')

    #-------------------------------------------------------------------------
    keys = sorted(dirrepo.listkeys('joe'))
    assert keys == [('joe', '1', joe1), ('joe', '2', joe2)]

    #-------------------------------------------------------------------------
    dirrepo.dropkey('joe', 1)
    assert [('joe', '2', joe2)] == sorted(dirrepo.listkeys('joe'))

    #-------------------------------------------------------------------------
    key = dirrepo.addkey('joe', 'zxcv')
    keys = sorted(dirrepo.listkeys('joe'))
    assert keys == [('joe', '2', joe2), ('joe', '3', 'zxcv')]
