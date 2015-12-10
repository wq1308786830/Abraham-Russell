# -*- coding: utf-8 -*-
# !/usr/bin/python

from flask import Blueprint, request, render_template, url_for
from apps.models.models import User

__author__ = 'Russell'

blog = Blueprint("blog", __name__)


@blog.route("/<username>&<password>")
def index(username, password):
    """

    :param password:
    :param username:
    :return:
    """

    print username, password
    # 创建session对象:
    # session = db_session()
    # 创建新User对象:
    # new_user = User(id=username, name=username)
    # 添加到session:
    # session.add(new_user)
    # simple query
    user = User.query.filter(User.name == 'a').first()
    print user.id + user.name
    # 提交即保存到数据库:
    # session.commit()
    # 关闭session:
    # session.close()
    return render_template("index.html")
