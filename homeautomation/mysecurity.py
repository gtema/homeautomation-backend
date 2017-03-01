# -*- coding: utf-8 -*-
import logging
import base64
from functools import wraps

from collections import OrderedDict

from flask import current_app, request, jsonify, _request_ctx_stack
from werkzeug.local import LocalProxy

__version__ = '0.0.1'

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

current_identity = LocalProxy(lambda: getattr(_request_ctx_stack.top,
                              'current_identity', None))

_sec = LocalProxy(lambda: current_app.extensions['mysec'])

CONFIG_EXT_DEFAULTS = {
    'SEC_LOGIN_URL': '/auth',
    'SEC_AUTH_DEFAULT_REALM': 'Login Required',
    'SEC_AUTH_USERNAME_KEY': 'username',
    'SEC_AUTH_PASSWORD_KEY': 'password',
    'SEC_AUTH_API_KEY': 'api_key',
}


def _auth_required(realm):
    """Verify the request authorization. Requires either Basic auth OR
    API_KEY be present in the Authorization header

    :param realm: an optional realm
    """
    authorization_header = request.headers.get('Authorization', None)

    if authorization_header is None:
        # https://www.httpwatch.com/httpgallery/authentication/
        raise MySecurityError('Authorization Required',
                              'Request does not contain an access token',
                              headers={
                                'WWW-Authenticate':
                                'API_KEY realm="%s"' %
                                current_app.config['SEC_AUTH_DEFAULT_REALM']})

    username, password, api_key = \
        _sec.process_request_auth_header(authorization_header)

    identity = None

    if api_key or (username and password):
        # Login using API_KEY
        identity = _sec.auth_callback(username, password, api_key)

    if identity is None:
        raise MySecurityError('Invalid Token', 'User does not exist')

    _request_ctx_stack.top.current_identity = identity


def auth_required():
    """View decorator that requires a valid authorization
    to be present in the request

    :param realm: an optional realm
    """
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            _auth_required(current_app.config['SEC_AUTH_DEFAULT_REALM'])
            return fn(*args, **kwargs)
        return decorator
    return wrapper


class MySecurityError(Exception):
    def __init__(self, error, description, status_code=401, headers=None):
        self.error = error
        self.description = description
        self.status_code = status_code
        self.headers = headers

    def __repr__(self):
        return 'MySecurityError: %s' % self.error

    def __str__(self):
        return '%s. %s' % (self.error, self.description)


class MySecurity(object):
    """MySecurity module to enable security with API_KEY
    """

    def __init__(self, app=None, auth_callback=None, post_login_callback=None):
        """

        :param app: application
        :param auth_callback: callback function to be called
                              for the user authentication
        :param post_login_callback: callback to be called
                                    after successfull login
        """

        self.auth_callback = auth_callback
        self.post_login_callback = post_login_callback

        self.login_response_callback = self.login_response_handler
        self.login_request_callback = self.login_request_handler

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        for k, v in CONFIG_EXT_DEFAULTS.items():
            app.config.setdefault(k, v)

        login_url = app.config.get('SEC_LOGIN_URL', None)

        if login_url:
            if self.login_request_callback == self.login_request_handler:
                assert self.auth_callback is not None, (
                    'an authentication_handler function must be defined when '
                    'using the built in authentication resource')

            login_url_options = app.config.get('SEC_AUTH_URL_OPTIONS',
                                               {'methods': ['POST', 'GET']})
            login_url_options.setdefault('view_func',
                                         self.login_request_callback)
            app.add_url_rule(login_url, **login_url_options)

        app.errorhandler(MySecurityError)(self.error_handler)

        if not hasattr(app, 'extensions'):  # pragma: no cover
            app.extensions = {}

        app.extensions['mysec'] = self

    def process_request_auth_header(self, authorization_header):
        """Process Authorization request header
        """
        logger.debug('Processing authorization data from request header {%s}',
                     authorization_header)

        tokens = authorization_header.split()

        if len(tokens) != 2:
            raise MySecurityError('Bad Request',
                                  'Unsupported authorization type')

        auth_type, auth_value = tokens[0], tokens[1]

        username = password = api_key = None

        if (auth_type == 'Basic'):
            # Basic authorization
            try:
                username, password = \
                    base64.b64decode(auth_value).decode().split(':', 1)
            except TypeError as e:
                raise MySecurityError('Bad Request',
                                      'Wrong authorization payload')
        elif (auth_type == 'API_KEY'):
            # API_KEY authorization
            api_key = auth_value

        return username, password, api_key

    def login_request_handler(self):
        """Process the login request
        """
        authorization_header = request.headers.get('Authorization', None)

        logger.debug(request.method)

        username, password, api_key = None, None, None
        # Auth criterias
        criteria_user = [username, password]
        criteria_api = [api_key]
        final_criteria = [criteria_user, criteria_api]

        if authorization_header is None:
            if (request.method == 'POST'):
                data = request.get_json()

                username = data.get(current_app.config.
                                    get('SEC_AUTH_USERNAME_KEY'), None)
                password = data.get(current_app.config.
                                    get('SEC_AUTH_PASSWORD_KEY'), None)
                criterion = [criteria_user, len(data) == 2]

                if not all(criterion):
                    # ONLY user data expected
                    raise MySecurityError('Bad Request',
                                          'Unsupported authorization type')
        else:
            username, password, api_key = \
                self.process_request_auth_header(authorization_header)

        if not any(final_criteria):
            raise MySecurityError('Bad Request',
                                  'Cannot process authorization credentials')

        identity = self.auth_callback(username, password, api_key)

        if identity:
            # found a user
            if self.post_login_callback is not None:
                # call a post_login callback if present
                self.post_login_callback(identity)
            return self.login_response_callback(identity)
        else:
            raise MySecurityError('Bad Request', 'Invalid credentials')

    def login_response_handler(self, identity):
        """ return data after login
        """
        return jsonify({
            'api_key': identity.api_key,
            'last_login_at': identity.last_login_at
            })

    def error_handler(self, error):
        """ Errorhandler
        """
        logger.error(error)
        return jsonify(OrderedDict([
            ('status_code', error.status_code),
            ('error', error.error),
            ('description', error.description),
        ])), error.status_code, error.headers
