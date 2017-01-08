from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cache import Cache
from flask_login import LoginManager
from flask_marshmallow import Marshmallow
from flask_cors import CORS


app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py')
CORS(app)

lm = LoginManager()
lm.init_app(app)

db = SQLAlchemy(app)
ma = Marshmallow(app)
cache = Cache(app)


from .api import api_bp
''' Can import API only after declaring db and ma '''


app.register_blueprint(api_bp,  url_prefix='/api/v0')


from .views import *
