# -*- coding: utf-8 -*-
# !/usr/bin/python

from flask import Blueprint, request, render_template, url_for
from apps.database.database import db_session
from apps.models.models import User

__author__ = 'Russell'

blog = Blueprint("blog", __name__)


@blog.route("/")
def index():
    """

    :return:
    """

    return render_template("index.html")


@blog.route("/<id>&<username>")
def add_query(id, username):
    """

    :param id:
    :param username:
    :return:
    """

    # 创建session对象:
    session = db_session()
    if not session.query(User).filter(User.id == id):
        print username, id
        # 创建新User对象:
        new_user = User(id=id, name=username)
        # 添加到session:
        session.add(new_user)
    # simple query
    user = session.query(User).filter(User.name == 'a').first()
    print user.id + user.name
    # 提交即保存到数据库:
    session.commit()
    # 关闭session:
    session.close()

    return render_template("index.html")


@blog.route('/run_girl')
def run_girl():
    """
    svg跑步的小女孩
    :return:
    """
    return render_template('bezier_running_girl.html')
