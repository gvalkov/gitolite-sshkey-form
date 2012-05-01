#!/usr/bin/env python
# encoding: utf-8

import os
import git
import shutil

from os import environ
from os.path import join as pjoin, dirname

class GitError(Exception):
    pass

class GitAdmin(object):
    def __init__(self, workdir, repourl, branch='master',
                       author_name='Gitolite Publickey Form',
                       author_email='nobody@localhost',
                       overwrite=False):

        self.workdir = workdir
        self.repourl = repourl
        self.branch  = branch

        self.author_name  = author_name
        self.author_email = author_email

        self.overwrite = overwrite

        self.repo = self._setup()

    def write(self, fn, data):
        ''' Write :data to :fn relative to workding dir '''

        path = pjoin(self.repo.working_dir, fn)

        try: os.makedirs(dirname(path))
        except: pass

        with open(pjoin(self.repo.working_dir, fn), 'w') as fh:
            fh.write(data)

    def add(self, *args):
        ''' Add files to git index '''
        self.repo.index.add(args)

    def reset(self, commit='HEAD'):
        self.repo.head.reset(commit=commit, working_tree=True)

    def rm(self, *args):
        ''' Remove files - paths must be relative to working dir '''
        hashead = bool(self.repo.heads)

        for arg in args:
            if hashead and \
               self.isfileintree(arg,self.repo.head.commit.tree):
                self.repo.index.remove((arg,))
            p = pjoin(self.repo.working_dir, arg)
            os.unlink(p)

    def commit(self, msg):
        ''' Commit staged files '''

        # only way I found to make gitpython change the commit's author
        environ['GIT_AUTHOR_NAME' ] = self.author_name
        environ['GIT_AUTHOR_EMAIL'] = self.author_email

        self.repo.index.commit(msg)

    def tree(self, path):
        return self.repo.heads.master.commit.tree[path]

    def pull(self, *args, **kw):
        return self.repo.remotes.origin.pull(*args, **kw)

    def push(self, *args, **kw):
        return self.repo.remotes.origin.push(*args, **kw)

    def isfileintree(self, fn, tree):
        try: tree[fn]; return True
        except KeyError: return False

    def _setUp(self):
        try:
            repo = git.Repo(self.workdir)
        except (git.NoSuchPathError, git.InvalidGitRepositoryError):
            repo = False

        if repo and self._remotesEqual(repo):
            return repo
        else:
            return self._clone()

        if os.path.exists(self.workdir):
            if not self.overwrite:
                msg = 'Workdir is not a git repository and force=False: refusing to overwrite'
                raise GitoliteError(msg)
            else:
                shutil.rmtree(self.workdir)
                return self._clone()

    def _clone(self):
        try:
            return git.Repo.clone_from(self.repourl, self.workdir)
        except git.GitCommandError:
            msg = 'Could not clone remote "%s" to "%s"' % (self.repourl, self.workdir)
            raise GitError(msg)

    def _remotesequal(self, repo):
        ''' Check if repo's origin == self.repourl '''

        origin = [i for i in repo.remotes if i.name == 'origin'][0] # @todo
        return origin.url == self.repourl

