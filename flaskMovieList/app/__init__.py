"""
   Algorithms Wep API initialization point
   with creation Flask app, set up dashboard and configure logging
"""

import os
from logging.handlers import RotatingFileHandler
import logging

from flask import Flask
from flask_caching import Cache
from .config import Config

from flask_cors import CORS


# set up flask application
app = Flask(__name__)
app.config['BUNDLE_ERRORS'] = True
app.config['TESTING'] = Config.TESTING
app.config['TESTING'] = "simple"
app.config["CACHE_DEFAULT_TIMEOUT"] = Config.DATA_RELOAD_TIME
app.config["CACHE_TYPE"] = "simple"

# add CORS for frontend cross domain policy
cors = CORS(app)

cache = Cache(app)

# create and set up simple logging
if not app.config['TESTING']:
    try:
        if not os.path.exists('logs'):
            os.mkdir('logs')
    except Exception as error:
        print(repr(error))

    file_handler = RotatingFileHandler(Config.LOG_DIRRECTORY, maxBytes=Config.LOG_SIZE,
                                               backupCount=Config.LOG_BACKUP_COUNT)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)

    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)


def clear_cash():
    with app.app_context():
        cache.clear()


from . import routes, movieListLoader


