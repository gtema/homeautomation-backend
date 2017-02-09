############################################################################################
# JWT Functions for Authenticating Users via API
############################################################################################

from functools import wraps
import logging

from .models import user_datastore, db
from flask_security.utils import verify_password, login_user
# from flask_jwt import _jwt_required, current_identity, JWTError
# from flask import current_app, request, _request_ctx_stack

logger = logging.getLogger(__name__)

def authenticate(username=None, password=None, api_key=None):
    """Callback to search user using username and password OR api_key
    """
    logger.debug('Trying to authenticate user name=%s, key=%s', username, api_key)
    if username is not None:
        try:
            user = user_datastore.find_user(username=username)
        except KeyError:
            return None
        if user and username == user.username and not verify_password(password, user.password):
            return None
    elif username is None and api_key is not None:
        try:
            user = user_datastore.find_user(api_key=api_key)
        except KeyError:
            return None

    login_user(user, True)
    db.session.commit()
    return user

def load_user(id=None, api_key=None):
    """ Search the user using ID
    """
    logger.debug('Checking user with id=%s, key=%s', id, api_key)
    user = None
    if api_key is not None:
        logger.debug("Getting user using api_key " + api_key)
        user = user_datastore.find_user(api_key=api_key)
    elif id is not None:
        logger.debug("Getting user using id")
        user = user_datastore.find_user(id=id)
    return user

# def authorize1(realm=None):
#     """ Wrapper decorator to authorize request using either API_KEY present in the request or JWT
#     """
#     def wrapper(fn):
#         @wraps(fn)
#         def decorator(*args, **kwargs):
#             # Try to authorize with api key first (if it is present in the request)
#             auth_header_value = request.headers.get('Authorization', None)
#             auth_header_prefix = 'API_KEY'.lower()
#
#             parts = str.split(auth_header_value)
#             user = None
#
#             # if Authorization header starts with API_KEY and has a single value afterwards
#             if parts[0].lower() == auth_header_prefix and 2 == len(parts):
#                 # try to load user using the api_key
#                 user = load_user_api_key(parts[1])
#
#             # If the user with the api_key found
#             if user is not None:
#                 # push the user into the request context and return
#                 _request_ctx_stack.top.current_identity = user
#                 return fn(*args, **kwargs)
#             else:
#                 logger.warning("No user found using the API_KEY, continue using JWT")
#
#             # and now try to login using JWT
#             try:
#                 _jwt_required(realm or current_app.config['JWT_DEFAULT_REALM'])
#             except JWTError as e:
#                 raise e
#             return fn(*args, **kwargs)
#         return decorator
#     return wrapper
