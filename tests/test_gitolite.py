#!/usr/bin/env python
# encoding: utf-8

from tests.util import *

gitolite = Tests()

@gitolite.context
def createGitoliteRepo():
    repourl, aliases = createGitoliteGitRepo()
    workdir = mkdtemp()
    git = GitAdmin(workdir, repourl)
    gitolite = Gitolite(git, Mock())

    try:
        yield gitolite, aliases
    finally:
        shutil.rmtree(repourl)
        shutil.rmtree(workdir)

readkey = lambda g, a, n: open(g._keypath(a, n)).read()

@gitolite.test
def listkeys(gitolite, aliases):
    for alias in aliases:
        keys = list(gitolite.listkeys(alias))
        assert all( [len(i) == 3 for i in keys] )
        assert all( [type(i[1] == int) for i in keys] )

        assert all( [i[0] == alias for i in keys] )
        assert all( [i[2] == readkey(gitolite, alias, i[1]) for i in keys] )

        keys = list(gitolite.listkeys(alias, namesonly=True))
        assert all( [i[2] == None for i in keys] )
        assert all( [i[0] == alias for i in keys] )

@gitolite.test
def addkey_new(gitolite, aliases):
    gitolite.addkey('johndoe', 'asdf')
    fc = readkey(gitolite, 'johndoe', 0)
    assert fc == 'asdf'

    gitolite.addkey('johndoe', 'zxcv')
    fc = readkey(gitolite, 'johndoe', 1)
    assert fc == 'zxcv'

@gitolite.test
def addkey_existing(gitolite, aliases):
    alias = aliases[0]

    keys = list(gitolite.listkeys(alias, namesonly=True))
    next_key = int(max([i[1] for i in keys])) + 1

    gitolite.addkey(alias, 'asdf')

    fc = readkey(gitolite, alias, next_key)
    assert fc == 'asdf'

@gitolite.test
def dropkey(gitolite, aliases):
    for n, alias in enumerate(aliases):
        gitolite.dropkey(alias, n)
        assert not exists( gitolite._keypath(alias, n) )


if __name__ == '__main__':
    gitolite.main()
