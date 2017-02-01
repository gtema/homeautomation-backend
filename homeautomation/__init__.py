from flask import Flask
from flask_jwt import JWT
from flask_security import Security
from .authentication import *

def create_app(config=None):
    """
    Application factory to create the app
    """
    # cache = Cache(config={'CACHE_TYPE': 'simple'})
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('config')
    app.config.from_pyfile('config.py')
    app.config.from_envvar('FLASKR_SETTINGS', silent=True)
    if config is not None:
        app.config.from_object(config)

    # Initialize Database
    from homeautomation.models import db, user_datastore
    db.init_app(app)

    # Load API blueprint
    from .api_v1 import api_bp
    app.register_blueprint(api_bp,  url_prefix='/api/v0')

    # Initialize flask-security
    security = Security(app, user_datastore)
    jwt      = JWT(app, authenticate, load_user)

    return app
