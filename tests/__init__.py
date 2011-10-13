#!/usr/bin/env python
# encoding: utf-8

from attest import Tests

from test_git import git
from test_gitolite import gitolite
from test_util import utilt
#from test_app import *

tests = (
    utilt,
    git,
    gitolite,
)

all = Tests(tests)

if __name__ == '__main__':
    all.main()
