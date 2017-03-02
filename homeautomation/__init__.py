import os
import logging
from flask import Flask
from flask_security import Security
from flask_cors import CORS


def create_app(config=None):
    """
    Application factory to create the app
    """
    # cache = Cache(config={'CACHE_TYPE': 'simple'})
    app = Flask(__name__, instance_relative_config=True)
    # app.config.from_object('config')
    # Read instance config
    app.config.from_pyfile('config.py')
    # Read ${APP_SETTINGS} config defined in root/config.py
    app.config.from_object(os.environ.get('APP_SETTINGS', 'config.Local'))
    # Read from config file given in the ${FLASKR_SETTINGS}
    app.config.from_envvar('FLASKR_SETTINGS', silent=True)
    # Read config given as a parameter
    if config is not None:
        app.config.from_object(config)

    app.logger.setLevel(logging.INFO)

    # Initialize Database
    from homeautomation.models import db, user_datastore
    db.init_app(app)

    # Load API blueprint
    from .api_v1 import api_bp
    app.register_blueprint(api_bp,  url_prefix='/api/v0')

    # Initialize flask-security
    security = Security(app, user_datastore)

    from .mysecurity import MySecurity
    from .authentication import authenticate, post_login

    sec = MySecurity(app=app, auth_callback=authenticate,
                     post_login_callback=post_login)

    CORS(app)

    return app
