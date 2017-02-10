############################################################################################
# JWT Functions for Authenticating Users via API
############################################################################################

from functools import wraps
import logging

from .models import user_datastore, db
from flask_security.utils import verify_password, login_user


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def authenticate(username=None, password=None, api_key=None):
    """Callback to search user using username and password OR api_key
    """
    logger.debug('Trying to authenticate user name=%s, key=%s', username, api_key)
    if api_key is not None:
        try:
            user = user_datastore.find_user(api_key=api_key)
        except KeyError:
            return None
    if username is not None:
        try:
            user = user_datastore.find_user(username=username)
        except KeyError:
            return None
        #verify user
        if user and username == user.username and not verify_password(password, user.password):
            return None

    return user

def post_login(identity):
    """ Callback to be called after authentification

    :param identity: found user
    """
    if identity is not None:
        login_user(identity, True)
        db.session.commit()
