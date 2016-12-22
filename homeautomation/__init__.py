from flask import Flask
from flask_sqlalchemy import SQLAlchemy
#from flask_cache import Cache
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
#cache = Cache(app)

from homeautomation import models, views 

@lm.user_loader
def load_user(user_id):
    ''' Load loggedin user from the DB'''
    print ('load_user ', user_id)
    return models.User.query.filter(models.User.id == user_id).first()

@lm.request_loader
def load_user_from_request(req):
    print ('load_user_from_request')
    api_key = req.args.get('api_key')
    if (api_key):
        return models.User.query.filter(models.User.id == 1).first()
    return None

from homeautomation.api import api_bp
app.register_blueprint(api_bp,  url_prefix = '/api/v0')
