# -*- coding: utf-8 -*-
import datetime as dt

from flask.ext.login import UserMixin

from farmsList.extensions import bcrypt
from farmsList.database import (
    Column,
    db,
    Model,
    ReferenceCol,
    relationship,
    SurrogatePK,
)

class Role(SurrogatePK, Model):
    __tablename__ = 'roles'
    name = Column(db.String(80), unique=True, nullable=False)
    user_id = ReferenceCol('users', nullable=True)
    user = relationship('User', backref='roles')

    def __init__(self, name, **kwargs):
        db.Model.__init__(self, name=name, **kwargs)

    def __repr__(self):
        return '<Role({name})>'.format(name=self.name)

class Email(SurrogatePK, Model):
    __tablename__ = 'emails'
    sender = Column(db.String(80), nullable=False)
    recipients = Column(db.String(2000), nullable=False)
    body = Column(db.String(6250000), nullable=False)
    time_sent = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)

    def __init__(self, sender, recipients, body, **kwargs):
        db.Model.__init__(self, sender=sender, recipients=recipients, body=body, **kwargs)

    def __repr__(self):
        return '<Email(From:{sender};To:{recipient};Body:{body})>'.format(sender=self.sender, recipient=self.recipient, body=self.body)

class User(UserMixin, SurrogatePK, Model):
    __tablename__ = 'users'
    username = Column(db.String(80), unique=True, nullable=False)
    email = Column(db.String(80), unique=True, nullable=False)
    #: The hashed password
    password = Column(db.String(128), nullable=True)
    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    first_name = Column(db.String(30), nullable=True)
    last_name = Column(db.String(30), nullable=True)
    active = Column(db.Boolean(), default=False)
    is_admin = Column(db.Boolean(), default=False)

    def __init__(self, username, email, password=None, **kwargs):
        db.Model.__init__(self, username=username, email=email, **kwargs)
        if password:
            self.set_password(password)
        else:
            self.password = None

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, value):
        return bcrypt.check_password_hash(self.password, value)

    @property
    def full_name(self):
        return "{0} {1}".format(self.first_name, self.last_name)

    def __repr__(self):
        return '<User({username!r})>'.format(username=self.username)
