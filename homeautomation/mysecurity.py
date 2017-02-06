# -*- coding: utf-8 -*-

# Fork of the Flask-JWT
import logging
import warnings
from functools import wraps

# from collections import OrderedDict
from datetime import datetime, timedelta

import jwt

from flask import current_app, request, jsonify, _request_ctx_stack
from werkzeug.local import LocalProxy
from flask_jwt import JWT, JWTError, CONFIG_DEFAULTS, encode_token, \
    _default_jwt_headers_handler, _default_jwt_payload_handler,\
    _default_jwt_encode_handler, _default_jwt_decode_handler,\
    _default_jwt_error_handler

__version__ = '0.0.1'

logger = logging.getLogger(__name__)

current_identity = LocalProxy(lambda: getattr(_request_ctx_stack.top, 'current_identity', None))

_jwt = LocalProxy(lambda: current_app.extensions['jwt'])

CONFIG_EXT_DEFAULTS = {
    # 'JWT_DEFAULT_REALM': 'Login Required',
    # 'JWT_AUTH_URL_RULE': '/auth',
    # 'JWT_AUTH_ENDPOINT': 'jwt',
    # 'JWT_AUTH_USERNAME_KEY': 'username',
    # 'JWT_AUTH_PASSWORD_KEY': 'password',
    'JWT_AUTH_API_KEY': 'api_key',
    # 'JWT_ALGORITHM': 'HS256',
    # 'JWT_LEEWAY': timedelta(seconds=10),
    'JWT_AUTH_HEADER_PREFIX': 'JWT',
    'JWT_AUTH_API_KEY_HEADER_PREFIX': 'API_KEY',
    # 'JWT_EXPIRATION_DELTA': timedelta(seconds=300),
    # 'JWT_NOT_BEFORE_DELTA': timedelta(seconds=0),
    # 'JWT_VERIFY_CLAIMS': ['signature', 'exp', 'nbf', 'iat'],
    # 'JWT_REQUIRED_CLAIMS': ['exp', 'iat', 'nbf']
}


def _default_request_handler():
    auth_header_value = request.headers.get('Authorization', None)
    auth_jwt_header_prefix = current_app.config['JWT_AUTH_HEADER_PREFIX']
    auth_key_header_prefix = current_app.config['JWT_AUTH_API_KEY_HEADER_PREFIX']

    if not auth_header_value:
        return

    tokens = dict(item.split() for item in auth_header_value.split(","))

    if auth_key_header_prefix in tokens:
        # do we have an API_KEY auth header?
        return auth_key_header_prefix, tokens[auth_key_header_prefix]

    elif auth_jwt_header_prefix in tokens:
        # do we have an JWT auth header?
        return auth_jwt_header_prefix, tokens[auth_jwt_header_prefix]

    # do not care of other auth methods
    raise JWTError('Invalid JWT header', 'Unsupported authorization type')


def _default_auth_request_handler():
    data = request.get_json()
    username = data.get(current_app.config.get('JWT_AUTH_USERNAME_KEY'), None)
    password = data.get(current_app.config.get('JWT_AUTH_PASSWORD_KEY'), None)
    api_key = data.get(current_app.config.get('JWT_AUTH_API_KEY'), None)
    criterion_username = [username, password, len(data) == 2]
    criterion_api_key = [api_key, len(data) == 1]

    if not all(criterion_username) and not all(criterion_api_key):
        raise JWTError('Bad Request', 'Invalid credentials')

    identity = _jwt.authentication_callback(username, password, api_key)

    if identity:
        access_token = _jwt.jwt_encode_callback(identity)
        return _jwt.auth_response_callback(access_token, identity)
    else:
        raise JWTError('Bad Request', 'Invalid credentials')


def _default_auth_response_handler(access_token, identity):
    return jsonify({
        'access_token': access_token.decode('utf-8'),
        'api_key': identity.api_key
        })


def _jwt_required(realm):
    """Does the actual work of verifying the JWT data in the current request.
    This is done automatically for you by `jwt_required()` but you could call it manually.
    Doing so would be useful in the context of optional JWT access in your APIs.

    :param realm: an optional realm
    """
    auth_type, token = _jwt.request_callback()

    if token is None:
        raise JWTError('Authorization Required', 'Request does not contain an access token',
                       headers={'WWW-Authenticate': 'JWT realm="%s"' % realm})

    identity = None
    if auth_type.lower() == current_app.config['JWT_AUTH_API_KEY_HEADER_PREFIX'].lower():
        # Login using API_KEY
        identity = _jwt.identity_callback(None, token)

    elif identity is None and auth_type.lower() == current_app.config['JWT_AUTH_HEADER_PREFIX'].lower():
        # Login using JWT
        try:
            payload = _jwt.jwt_decode_callback(token)
        except jwt.InvalidTokenError as e:
            raise JWTError('Invalid token', str(e))

        identity = _jwt.identity_callback(payload['identity'], None)

    if identity is None:
        raise JWTError('Invalid JWT', 'User does not exist')

    _request_ctx_stack.top.current_identity = identity


def auth_required(realm=None):
    """View decorator that requires a valid JWT token to be present in the request

    :param realm: an optional realm
    """
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            _jwt_required(realm or current_app.config['JWT_DEFAULT_REALM'])
            return fn(*args, **kwargs)
        return decorator
    return wrapper


class MySecurity(JWT):
    """Extension of the flask-jwt module to support authorization per both JWT and api_key
    """

    def __init__(self, app=None, authentication_handler=None, identity_handler=None):
        self.authentication_callback = authentication_handler
        self.identity_callback = identity_handler

        self.auth_response_callback = _default_auth_response_handler
        self.auth_request_callback = _default_auth_request_handler
        self.jwt_encode_callback = _default_jwt_encode_handler
        self.jwt_decode_callback = _default_jwt_decode_handler
        self.jwt_headers_callback = _default_jwt_headers_handler
        self.jwt_payload_callback = _default_jwt_payload_handler
        self.jwt_error_callback = _default_jwt_error_handler
        self.request_callback = _default_request_handler

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        for k, v in CONFIG_DEFAULTS.items():
            app.config.setdefault(k, v)
        for k, v in CONFIG_EXT_DEFAULTS.items():
            app.config.setdefault(k, v)
        app.config.setdefault('JWT_SECRET_KEY', app.config['SECRET_KEY'])

        auth_url_rule = app.config.get('JWT_AUTH_URL_RULE', None)

        if auth_url_rule:
            if self.auth_request_callback == _default_auth_request_handler:
                assert self.authentication_callback is not None, (
                    'an authentication_handler function must be defined when using the built in '
                    'authentication resource')

            auth_url_options = app.config.get('JWT_AUTH_URL_OPTIONS', {'methods': ['POST']})
            auth_url_options.setdefault('view_func', self.auth_request_callback)
            app.add_url_rule(auth_url_rule, **auth_url_options)

        app.errorhandler(JWTError)(self._jwt_error_callback)

        if not hasattr(app, 'extensions'):  # pragma: no cover
            app.extensions = {}

        app.extensions['jwt'] = self
