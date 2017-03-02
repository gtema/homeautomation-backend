from .models import user_datastore, db
from flask import current_app
from flask_security.utils import verify_password, login_user


def authenticate(username=None, password=None, api_key=None):
    """Callback to search user using username and password OR api_key
    """
    current_app.logger.debug('Trying to authenticate user name=%s, key=%s',
                             username, api_key)
    user = None
    if api_key is not None:
        try:
            user = user_datastore.find_user(api_key=api_key)
        except:
            return None
    if username is not None:
        try:
            user = user_datastore.find_user(username=username)
        except:
            return None
        # verify user
        if user and username == user.username and \
                not verify_password(password, user.password):
            return None

    return user


def post_login(identity):
    """ Callback to be called after authentification

    :param identity: found user
    """
    if identity is not None:
        try:
            login_user(identity, True)
            db.session.commit()
        except:
            return None
