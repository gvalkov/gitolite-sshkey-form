#!/usr/bin/env python
# encoding: utf-8

from websshkey import util
from tests.util import *

utilt = Tests()

@utilt.test
def pairwise():
    i = util.pairwise((1,2,3))

    assert i.next() == (1,2)
    assert i.next() == (2,3)

    i = util.pairwise((1,))
    with raises(StopIteration):
        i.next()

@utilt.test
def onlyint():
    assert util.onlyint(1) == 1
    assert util.onlyint('1') == 1
    assert util.onlyint('a') == None

@utilt.test
def nextinseq():
    n = util.nextinseq

    assert n([0, 1, 3]) == 2
    assert n([0, 'asdf', '3', 5]) == 1
    assert n([0, 1, 'asdf', 2, '3', 5]) == 4
    assert n([]) == 0
    assert n(['a', 'b', 'c']) == 0

@utilt.test
def iskeyvalid():
    p = mktemp()
    sshkeyGen(p, True)
    assert util.iskeyvalid(open(p+'.pub').read())

    sshkeyGen(p, False)
    assert not util.iskeyvalid(open(p+'.pub').read())

    os.unlink(p) # big deal

@utilt.test
def listkeys64():
    keys = (('a', 'zxcv', 'asdf'),)

    for a, b, c in util.listkeys64(keys):
        assert util.urlsafe_b64decode(b) == keys[0][1]


if __name__ == '__main__':
    utilt.main()
