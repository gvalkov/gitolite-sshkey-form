from __future__ import absolute_import
from __future__ import print_function

from . views import app, configure
from . __main__ import RemoteUserMiddleware, TestUserMiddleware


#-----------------------------------------------------------------------------
app.config.from_envvar('WEBSSHKEY_CONFIG')
# app.wsgi_app = TestUserMiddleware(app.wsgi_app, 'joe')
app.wsgi_app = RemoteUserMiddleware(app.wsgi_app)
