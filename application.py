# -*- coding: utf-8 -*-
# !/usr/bin/python

import os
from flask import Flask, g, json
from apps.blogs.view import blog
from apps.database.database import db_session
from apps.tasks import make_celery

PROJECT_PATH = os.path.dirname(__file__)


def create_app():
    app = Flask(__name__)

    config_file = os.path.abspath(os.path.join(PROJECT_PATH, 'etc/config.py'))
    app.config.from_pyfile(config_file)

    app.config.update(
        CELERY_BROKER_URL='redis://localhost:6379',
        CELERY_RESULT_BACKEND='redis://localhost:6379'
    )

    config_celery(app)
    config_log(app)
    config_db(app)
    config_route(app)

    app.logger.warn("app准备好了")

    return app


def config_log(app):
    import logging
    from logging.handlers import RotatingFileHandler

    format = '[%(asctime)s %(levelname)s]: %(message)s [in %(pathname)s:%(lineno)d]'
    log_file = app.config.get("LOG_FILE")
    if log_file:
        handler = RotatingFileHandler(
            log_file,
            maxBytes=10000,
            backupCount=10,
        )
        handler.setFormatter(logging.Formatter(format))
        app.logger.addHandler(handler)

    debug = app.debug
    if not debug:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(format))
        app.logger.addHandler(handler)
        app.logger.setLevel(logging.WARN)

    app.logger.warn("xxxx")


def config_db(app):
    """
    配置数据库session创建
    :param app:
    :return:
    """

    @app.before_request
    def before_request():
        g.data_session = db_session()

    @app.teardown_request
    def teardown_request(exception):

        if hasattr(g, 'data_session'):
            g.data_session.close()
        if exception:
            print 'on app.teardown_request exception===', exception


def config_route(app):
    """
    配置 url
    :param app:
    :return:
    """
    common_prefix = ''
    app.register_blueprint(blog, url_prefix=common_prefix)

    @app.errorhandler(400)
    def handler_400(error):
        return json.dumps(dict(message='参数不能为空:' + str(error.args))), 400


def config_celery(app):
    """

    :param app:
    :return:
    """
    celery = make_celery(app)

    @celery.task()
    def add_together(a, b):
        return a + b
