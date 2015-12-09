# -*- coding: utf-8 -*-
# !/usr/bin/python
from datetime import datetime

from flask.ext.sqlalchemy import BaseQuery
from werkzeug.security import generate_password_hash

from apps.blogs.types import DenormalizedText
from extensions import db

__author__ = 'Russell'


class UserQuery(BaseQuery):
    def from_identity(self, identity):
        """
        Loads user from flaskext.principal.Identity instance and
        assigns permissions from user.

        A "user" instance is monkeypatched to the identity instance.

        If no user found then None is returned.
        """

        try:
            user = self.get(int(identity.id))
        except (ValueError, TypeError):
            user = None

        if user:
            identity.provides.update(user.provides)

        identity.user = user

        return user

    def authenticate(self, login, password):

        user = self.filter(db.or_(User.username == login,
                                  User.email == login)).first()

        if user:
            authenticated = user.check_password(password)
        else:
            authenticated = False

        return user, authenticated

    def authenticate_openid(self, email, openid):

        user = self.filter(User.email == email).first()

        if user:
            authenticated = user.check_openid(openid)
        else:
            authenticated = False

        return user, authenticated


class User(db.Model):
    __tablename__ = "users"

    query_class = UserQuery

    # user roles
    MEMBER = 100
    MODERATOR = 200
    ADMIN = 300

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Unicode(60), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    karma = db.Column(db.Integer, default=0)
    date_joined = db.Column(db.DateTime, default=datetime.utcnow)
    activation_key = db.Column(db.String(80), unique=True)
    role = db.Column(db.Integer, default=MEMBER)
    receive_email = db.Column(db.Boolean, default=False)
    email_alerts = db.Column(db.Boolean, default=False)
    followers = db.Column(DenormalizedText())
    following = db.Column(DenormalizedText())

    _password = db.Column("password", db.String(80))
    _openid = db.Column("openid", db.String(80), unique=True)

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)

    def __str__(self):
        return self.username

    def __repr__(self):
        return "<%s>" % self

    def _get_password(self):
        return self._password

    def _set_password(self, password):
        self._password = generate_password_hash(password)

    password = db.synonym("_password",
                          descriptor=property(_get_password,
                                              _set_password))
