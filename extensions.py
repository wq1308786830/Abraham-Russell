#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask.ext.openid import OpenID
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.cache import Cache

__all__ = ['oid', 'db', 'cache']

oid = OpenID()
db = SQLAlchemy()
cache = Cache()

