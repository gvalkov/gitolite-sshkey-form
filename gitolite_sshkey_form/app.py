#!/usr/bin/env python
# encoding: utf-8

from flask import Flask

app = Flask('gitolite_sshkey_form')
app.debug = True

import gitolite_sshkey_form.views
