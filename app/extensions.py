# -*- coding: utf-8 -*-

from flask_sqlalchemy import SQLAlchemy
from raven.contrib.flask import Sentry

redis_cache = {}

db = SQLAlchemy()

sentry = Sentry()
