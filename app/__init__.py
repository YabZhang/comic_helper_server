#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import logging

from flask import Flask
from flask_redis import FlaskRedis

import config
from config import Config
from app.extensions import redis_cache, db, sentry


def static_init_redis():
    """静态方式初始化 redis"""
    for prefix in Config.REDIS_URL_PREFIX:
        redis_cache[prefix] = FlaskRedis(config_prefix=prefix)


static_init_redis()


def init_blueprints(app):
    """
        注册 blueprints

        需要初始化好本文件的全局变量后调用，否则 blueprint 内无法 import 本文件的变量
    """
    return


def init_redis(app):
    for prefix, flask_redis in list(redis_cache.items()):
        flask_redis.init_app(app)

    app.extensions['redis_cache'] = redis_cache
    print(("init rediss:", list(redis_cache.keys())))


def init_db(app):
    db.init_app(app)


def init_sentry(app):
    sentry.init_app(
        app, logging=True, level=logging.ERROR,
        dsn=config.SENTRY_DSN_URL
    )


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)
    Config.init_app(app)

    init_db(app)

    # 初始化好本文件参数才能注册 blueprint
    init_blueprints(app)

    init_redis(app)
    if not config.DEBUG:
        init_sentry(app)

    return app
