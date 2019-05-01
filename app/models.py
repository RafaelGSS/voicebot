from datetime import datetime

from .base import db


class Requests(db.Model):
    __tablename__ = 'requests'
    __bind_key__ = 'local'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String(255), nullable=False)
    request = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<request %r>' % self.request

    @classmethod
    def _insert(cls, type, request, autocommit=True):
        obj = cls(type=type, request=request)
        if autocommit:
            db.session.add(obj)
            db.session.commit()
        return request

    @classmethod
    def insert_city(cls, city, autocommit=True):
        return cls._insert(type='CITY', request=city, autocommit=autocommit)

    @classmethod
    def insert_state(cls, state, autocommit=True):
        return cls._insert(type='STATE', request=state, autocommit=autocommit)

    @classmethod
    def insert_date(cls, date, autocommit=True):
        return cls._insert(type='DATE', request=date, autocommit=autocommit)
