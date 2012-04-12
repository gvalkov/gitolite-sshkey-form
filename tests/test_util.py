#!/usr/bin/env python
# encoding: utf-8

from websshkey import util
from tests.util import *


def test_pairwise():
    i = util.pairwise((1,2,3))

    assert i.next() == (1,2)
    assert i.next() == (2,3)

    i = util.pairwise((1,))
    with raises(StopIteration):
        i.next()

def test_onlyint():
    assert util.onlyint(1) == 1
    assert util.onlyint('1') == 1
    assert util.onlyint('a') == None

def test_nextinseq():
    n = util.nextinseq

    assert n([0, 1, 3]) == 2
    assert n([0, 'asdf', '3', 5]) == 1
    assert n([0, 1, 'asdf', 2, '3', 5]) == 4
    assert n([]) == 0
    assert n(['a', 'b', 'c']) == 0

def test_iskeyvalid():
    p = mktemp()
    sshkeyGen(p, True)
    assert util.iskeyvalid(open(p+'.pub').read())

    sshkeyGen(p, False)
    assert not util.iskeyvalid(open(p+'.pub').read())

    os.unlink(p) # big deal

def test_listkeys64():
    keys = (('a', 'zxcv', 'asdf'),)

    for a, b, c in util.listkeys64(keys):
        assert util.urlsafe_b64decode(b) == keys[0][1]

def test_splitkey():
    assert util.splitkey('joe@1.pub')  == ('joe', '1')
    assert util.splitkey('joe@pc.pub') == ('joe', 'pc')
    assert util.splitkey('joe.pub')    == ('joe', None)

def test_joinkey():
    assert util.joinkey('joe', 1)  == 'joe@1.pub'
    assert util.joinkey('joe', None)  == 'joe.pub'
