#!/usr/bin/env python
# encoding: utf-8

from tests.util import *

git = Tests()

@git.context
def createRepo():
    repourl = createGitRepo()
    workdir = mkdtemp()
    git = GitAdmin(workdir, repourl)

    try:
        yield repourl, workdir, git
    finally:
        shutil.rmtree(repourl)
        shutil.rmtree(workdir)

@git.test
def isgit(repourl, workdir, git):
    assert os.path.isdir('%s/.git' % workdir)

@git.test
def write(repourl, workdir, git):
    content = 'asdf zxcv 123'
    git.write('file1', content)
    git.write('files/1', content)

    fp1 = pjoin(git.repo.working_dir, 'file1')
    fp2 = pjoin(git.repo.working_dir, 'files/1')

    assert isfile(fp1)
    assert isfile(fp2)

    assert open(fp1).read() == content
    assert open(fp2).read() == content

@git.test
def add(repourl, workdir, git):
    [git.write(i, 'asdf') for i in '123']
    git.add('1', '2', '3')

    blobs = list(git.repo.index.iter_blobs())
    blobs = [i[1].name for i in blobs]

    assert sorted(blobs) == ['1', '2', '3']

@git.test
def rm(repourl, workdir, git):
    git.write('file1', 'asdf')
    git.rm('file1')
    assert not exists( pjoin(git.repo.working_dir, 'file1') )

    git.write('file2', 'asdf')
    git.add('file2')
    git.commit('ign')
    git.rm('file2')

    assert not exists( pjoin(git.repo.working_dir, 'file2') )

@git.test
def commit(repourl, workdir, git):
    add(repourl, workdir, git)

    msg   = 'commit msg'
    name  = 'author'
    email = 'email'

    git.commit(msg)
    commit = git.repo.commit('HEAD')

    assert commit.message == msg
    #assert commit.author.name == name
    #assert commit.author.email == email

    blobs = list(commit.tree.traverse())
    blobs = [i.name for i in blobs]

    assert sorted(blobs) == ['1', '2', '3']


if __name__ == '__main__':
    git.main()
