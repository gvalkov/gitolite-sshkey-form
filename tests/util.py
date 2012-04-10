#!/usr/bin/env python
# encoding: utf-8

import os, shutil
import random, string

from pytest import raises, set_trace
from mock import Mock

from tempfile import mktemp, mkdtemp, NamedTemporaryFile
from subprocess import Popen, check_call, call
from os.path import join as pjoin, isfile, exists
from collections import namedtuple

from websshkey.gitadmin import GitAdmin
from websshkey.gitolite import Gitolite

devnull = open(os.devnull, 'w')

def createGitRepo():
    workdir = mkdtemp()

    cmd = ('git', 'init', workdir)
    check_call(cmd, stdout=devnull, stderr=devnull)

    return workdir

def sshkeyGen(path, real=True, bits=768):
    if real:
        cmd = ('ssh-keygen', '-q', '-b', str(bits), '-N', '', '-f', path)
        check_call(cmd, stdout=devnull, stderr=devnull)
    else:
        s = random.sample(string.letters, 50)
        with open(path + '.pub', 'w') as fh:
            fh.write(''.join(s))

def createGitoliteGitRepo(users=2, keysperuser=2, realkeys=False):
    ''' Create a semi-realistic gitolite repo for testing purposes '''

    repourl = createGitRepo()

    keydir = pjoin(repourl, Gitolite.keydir)
    os.makedirs(keydir)

    aliases = []
    for n in range(0, users):
        alias = random.sample(string.lowercase, 10)
        aliases.append(''.join(alias))

    for alias in aliases:
        for n in range(0, keysperuser):
            p = pjoin(keydir, '%s@%s' % (alias, n))
            sshkeyGen(p, realkeys)

    for f in os.listdir(keydir):
        if not f.endswith('.pub'):
            os.unlink(pjoin(keydir, f))

    cmd = ('git', 'add', '-A')
    check_call(cmd, cwd=keydir)

    cmd = ('git', 'commit', '-q', '-m', '++')
    check_call(cmd, cwd=keydir)

    return repourl, aliases
