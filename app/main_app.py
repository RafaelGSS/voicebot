from flask import Flask

from . import base
from .base import db
from .interpreter import Interpreter
from routes import api


def create_app():
    app = Flask('voicebot')
    app.config.from_object('app.settings')

    base.init_app(app)

    @app.before_first_request
    def create_db():
        db.create_all()

    app.extensions['interpreter'] = Interpreter()

    app.register_blueprint(api.bp, url_prefix='/api/voice')

    return app
