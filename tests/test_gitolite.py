#!/usr/bin/env python
# encoding: utf-8

from tests.util import *


R = namedtuple('R', ('gitolite', 'aliases'))
readkey = lambda g, a, n: open(g._keypath(a, n)).read()


def pytest_funcarg__r(request):
    repourl, aliases = createGitoliteGitRepo()
    workdir = mkdtemp()
    git = GitAdmin(workdir, repourl)
    gitolite = Gitolite(git, Mock())

    def finalize():
        shutil.rmtree(repourl)
        shutil.rmtree(workdir)

    request.addfinalizer(finalize)
    return R(gitolite, aliases)


def listkeys(r):
    for alias in r.aliases:
        keys = list(r.gitolite.listkeys(alias))
        assert all( [len(i) == 3 for i in keys] )
        assert all( [type(i[1] == int) for i in keys] )

        assert all( [i[0] == alias for i in keys] )
        assert all( [i[2] == readkey(r.gitolite, alias, i[1]) for i in keys] )

        keys = list(r.gitolite.listkeys(alias, namesonly=True))
        assert all( [i[2] == None for i in keys] )
        assert all( [i[0] == alias for i in keys] )


def test_addkey_new(r):
    r.gitolite.addkey('johndoe', 'asdf')
    fc = readkey(r.gitolite, 'johndoe', 0)
    assert fc == 'asdf'

    r.gitolite.addkey('johndoe', 'zxcv')
    fc = readkey(r.gitolite, 'johndoe', 1)
    assert fc == 'zxcv'


def test_addkey_existing(r):
    alias = r.aliases[0]

    keys = list(r.gitolite.listkeys(alias, namesonly=True))
    next_key = int(max([i[1] for i in keys])) + 1

    r.gitolite.addkey(alias, 'asdf')

    fc = readkey(r.gitolite, alias, next_key)
    assert fc == 'asdf'


def test_dropkey(r):
    for n, alias in enumerate(r.aliases):
        r.gitolite.dropkey(alias, n)
        assert not exists( r.gitolite._keypath(alias, n) )

