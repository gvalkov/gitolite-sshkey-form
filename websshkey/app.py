#!/usr/bin/env python
# encoding: utf-8

from flask import Flask

app = Flask('websshkey')
app.debug = True

import websshkey.views
