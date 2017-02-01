############################################################################################
# JWT Functions for Authenticating Users via API
############################################################################################

from .models import user_datastore, db
from flask_security.utils import verify_password, login_user

# https://github.com/graup/flask-restless-security/blob/master/server.py
def authenticate(username, password):
    try:
        user = user_datastore.find_user(username=username)
    except KeyError:
        return None
    if user and username == user.username and verify_password(password, user.password):
        login_user(user, True)
        db.session.commit()
        return user
    return None

def load_user(payload):
    user = user_datastore.find_user(id=payload['identity'])
    return user
