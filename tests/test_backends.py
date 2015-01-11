# -*- coding: utf-8; -*-

import os
import pytest
import logging

from pathlib import Path
from sh import mkdir, touch, git

from websshkey.backends import Directory, Gitolite
from utils import sshkeygen

# stream = logging.StreamHandler()
# stream.setLevel(logging.INFO)
# logging.getLogger().setLevel(logging.INFO)
# logging.getLogger().addHandler(stream)
# shlog = logging.getLogger('sh')
# shlog.setLevel(logging.INFO)

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
    git('push', 'origin', 'HEAD', '--force', _cwd='%s/workdir' % tmpdir)

    repo = Gitolite(Path(str(tmpdir), 'workdir'), 'file:///%s/bare' % tmpdir, 'Gitolite Tests <t@t.t>')
    yield repo


#-----------------------------------------------------------------------------
def test_dit_create(tmpdir):
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


#-----------------------------------------------------------------------------
def test_git_create(gitrepo):
    pass

def test_git_basic(gitrepo):
    joe1 = sshkeygen(gitrepo.workdir / 'joe@1')
    joe2 = sshkeygen(gitrepo.workdir / 'joe@2')

    #-------------------------------------------------------------------------
    gitrepo.addkey('joe', joe1)
    gitrepo.addkey('joe', joe2)

    #-------------------------------------------------------------------------
    assert gitrepo.keyexists('joe', joe1)
    assert gitrepo.keyexists('joe', joe2)
    assert not gitrepo.keyexists('joe', 'asdf')

    #-------------------------------------------------------------------------
    keys = sorted(gitrepo.listkeys('joe'))
    assert keys == [('joe', '0', joe1), ('joe', '1', joe2)]

    #-------------------------------------------------------------------------
    gitrepo.dropkey('joe', 0)
    assert [('joe', '1', joe2)] == sorted(gitrepo.listkeys('joe'))

    #-------------------------------------------------------------------------
    key = gitrepo.addkey('joe', 'zxcv1')
    key = gitrepo.addkey('joe', 'zxcv2')
    keys = sorted(gitrepo.listkeys('joe'))
    assert keys == [('joe', '1', joe2), ('joe', '2', 'zxcv1'), ('joe', '3', 'zxcv2')]
