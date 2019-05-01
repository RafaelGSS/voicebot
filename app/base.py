from flask import current_app
from flask_caching import Cache
from flask_sqlalchemy import SQLAlchemy
from raven.contrib.flask import Sentry
from werkzeug.local import LocalProxy

cache = Cache(config={'CACHE_TYPE': 'simple'})
db = SQLAlchemy()
sentry = Sentry()

interpreter = LocalProxy(lambda: current_app.extensions['interpreter'])


def init_app(app):
    cache.init_app(app)
    db.init_app(app)
    sentry.init_app(app)
