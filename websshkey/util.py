#!/usr/bin/env python
# encoding: utf-8

import os

from base64     import urlsafe_b64encode, urlsafe_b64decode
from types      import IntType, StringType
from itertools  import tee, izip
from subprocess import call
from tempfile   import NamedTemporaryFile
from contextlib import contextmanager, closing


def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return izip(a, b)

def onlyint(data):
    if type(data) == IntType: return data

    if type(data) == StringType:
        if data.isdigit(): return int(data)

def nextinseq(seq, start=0):
    ''' [0, 1, 3] -> 2
        [0, 'asdf', '3', 5] -> 1
    '''

    seq = map(onlyint, seq)
    seq = filter(lambda x: x != None, seq)

    if not seq: return start
    if len(seq) == 1: return seq[0] + 1

    i=0; j=0

    for i, j in pairwise(seq):
        if (j-i) > 1: return i + 1
    else:
        return j + 1

def iskeyvalid(key):
    ''' Check if a given ssh public key is valid '''
    devnull = open(os.devnull, 'w')

    with NamedTemporaryFile() as fh:
        fh.write(key) ; fh.flush()
        cmd = ('ssh-keygen', '-l', '-f', fh.name)
        ret = call(cmd, stdout=devnull, stderr=devnull)

    return ret == 0

def listkeys64(keys):
    for user, machine, key in keys:
        # joe.pub -> machine is None (which is lame)
        yield user, urlsafe_b64encode(str(machine)), key

