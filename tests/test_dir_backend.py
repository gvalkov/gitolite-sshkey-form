# -*- coding: utf-8; -*-

import pytest

from websshkey.backends import Directory
from utils import sshkeygen


@pytest.yield_fixture
def repo(tmpdir):
    repo = Directory(str(tmpdir))
    yield repo

def test_create(tmpdir):
    repo = Directory(str(tmpdir))

    with pytest.raises(Exception):
        Directory('/etc/fstab')

def test_dir_basic(repo):
    joe1 = sshkeygen(repo.workdir / 'joe@1')
    joe2 = sshkeygen(repo.workdir / 'joe@2')

    #-------------------------------------------------------------------------
    assert repo.keyexists('joe', joe1)
    assert not repo.keyexists('joe', 'asdf')

    #-------------------------------------------------------------------------
    keys = sorted(repo.listkeys('joe'))
    assert keys == [('joe', '1', joe1), ('joe', '2', joe2)]

    #-------------------------------------------------------------------------
    repo.dropkey('joe', 1)
    assert [('joe', '2', joe2)] == sorted(repo.listkeys('joe'))

    #-------------------------------------------------------------------------
    key = repo.addkey('joe', 'zxcv')
    keys = sorted(repo.listkeys('joe'))
    assert keys == [('joe', '2', joe2), ('joe', '3', 'zxcv')]
