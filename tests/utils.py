# -*- coding: utf-8; -*-

import os
import random
import string
import subprocess as sub


def sshkeygen(path, real=False, bits=768):
    if real:
        cmd = ['ssh-keygen', '-q', '-b', str(bits), '-N', '', '-f', str(path)]
        devnull = open(os.devnull, 'w')
        sub.check_call(cmd, stdout=devnull, stderr=devnull)
    else:
        s = random.sample(string.ascii_letters, 50)
        with path.with_suffix('.pub').open('w') as fh:
            fh.write(''.join(s).decode('utf8'))

    return path.with_suffix('.pub').open().read()
