# encoding: utf-8

from __future__ import absolute_import
from __future__ import print_function

import os
import pytest
import base64
from pathlib import Path

from .. import utils
from .  utils import sshkeygen


def test_pairwise():
    i = utils.pairwise((1,2,3))

    assert next(i) == (1,2)
    assert next(i) == (2,3)

    i = utils.pairwise((1,))
    with pytest.raises(StopIteration):
        next(i)

def test_toint():
    assert utils.toint(1) == 1
    assert utils.toint('1') == 1
    assert utils.toint('a') == None

def test_nextinseq():
    n = utils.nextinseq

    assert n() == 0
    assert n([0, 1, 2]) == 3
    assert n([0, 1, 3]) == 2
    assert n([0, 'asdf', 3, 5]) == 1
    assert n([0, 1, 'asdf', 2, '3', 5]) == 4
    assert n(['asdf', '3']) == 4
    assert n(['a', 'b', 'c']) == 0

def test_iskeyvalid(tmpdir):
    tmpdir = Path(str(tmpdir))
    sshkeygen(tmpdir/'test', real=True)
    assert utils.iskeyvalid((tmpdir/'test.pub').open().read())

    sshkeygen(tmpdir/'test', real=False)
    assert not utils.iskeyvalid((tmpdir/'test.pub').open().read())

def test_listkeys64():
    keys = [('a', 'zxcv', 'asdf')]

    for a, b, c in utils.listkeys64(keys):
        b64 = base64.urlsafe_b64decode(b.encode('utf8'))
        assert b64.decode('utf8') == keys[0][1]

def test_splitkey():
    assert utils.splitkey('joe@1.pub')  == ('joe', '1')
    assert utils.splitkey('joe@pc.pub') == ('joe', 'pc')
    assert utils.splitkey('joe.pub')    == ('joe', None)

def test_joinkey():
    assert utils.joinkey('joe', 1)  == 'joe@1.pub'
    assert utils.joinkey('joe', None)  == 'joe.pub'
