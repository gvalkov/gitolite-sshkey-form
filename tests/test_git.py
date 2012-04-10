#!/usr/bin/env python
# encoding: utf-8

from tests.util import *

R = namedtuple('R', ('repourl', 'workdir', 'git'))

def pytest_funcarg__r(request):
    repourl = createGitRepo()
    workdir = mkdtemp()
    git = GitAdmin(workdir, repourl)

    def finalize():
        shutil.rmtree(repourl)
        shutil.rmtree(workdir)

    request.addfinalizer(finalize)
    return R(repourl, workdir, git)


def test_isgit(r):
    assert os.path.isdir('%s/.git' % r.workdir)

def test_write(r):
    content = 'asdf zxcv 123'
    r.git.write('file1', content)
    r.git.write('files/1', content)

    fp1 = pjoin(r.git.repo.working_dir, 'file1')
    fp2 = pjoin(r.git.repo.working_dir, 'files/1')

    assert isfile(fp1)
    assert isfile(fp2)

    assert open(fp1).read() == content
    assert open(fp2).read() == content

def test_add(r):
    [r.git.write(i, 'asdf') for i in '123']
    r.git.add('1', '2', '3')

    blobs = list(r.git.repo.index.iter_blobs())
    blobs = [i[1].name for i in blobs]

    assert sorted(blobs) == ['1', '2', '3']

def test_rm(r):
    r.git.write('file1', 'asdf')
    r.git.rm('file1')
    assert not exists( pjoin(r.git.repo.working_dir, 'file1') )

    r.git.write('file2', 'asdf')
    r.git.add('file2')
    r.git.commit('ign')
    r.git.rm('file2')

    assert not exists( pjoin(r.git.repo.working_dir, 'file2') )

def test_commit(r):
    test_add(r)

    msg   = 'commit msg'
    name  = 'author'
    email = 'email'

    r.git.commit(msg)
    commit = r.git.repo.commit('HEAD')

    assert commit.message == msg
    #assert commit.author.name == name
    #assert commit.author.email == email

    blobs = list(commit.tree.traverse())
    blobs = [i.name for i in blobs]

    assert sorted(blobs) == ['1', '2', '3']
