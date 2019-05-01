from decouple import config

JSON_AS_ASCII = False
SQLALCHEMY_TRACK_MODIFICATIONS = False

SQLALCHEMY_DATABASE_URI = config('DB_URI')
SQLALCHEMY_BINDS = {
    'local': config('DB_LOCAL_URI'),
}

FLASK_PORT = config('FLASK_PORT', default=5000, cast=int)

SENTRY_DSN = config('SENTRY_DSN')