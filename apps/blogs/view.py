# -*- coding: utf-8 -*-
# !/usr/bin/python

from flask import Blueprint, request, render_template

__author__ = 'Russell'


blog = Blueprint("blog", __name__)


@blog.route("/")
def index():
    """

    :return:
    """
    return render_template("index.html")
