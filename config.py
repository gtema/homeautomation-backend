import os
DEBUG = False

SQLALCHEMY_ECHO = False

SECRET_KEY = 'asdcxzqw'


class Config(object):
    DEBUG = True
    SQLALCHEMY_ECHO = False
    SECRET_KEY = 'aVfBgth%w2d&eh!.'
    SQLALCHEMY_DATABASE_URI = 'sqlite://'

    SECURITY_CONFIRMABLE = True
    SECURITY_TRACKABLE = True
    SECURITY_REGISTERABLE = True
    SECURITY_RECOVERABLE = True
    # SECURITY_PASSWORD_HASH = 'plaintext'
    SECURITY_PASSWORD_HASH = 'sha512_crypt'
    SECURITY_PASSWORD_SALT = 'add_salt'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PORT = os.environ.get('PORT', 5000)
    SEC_LOGIN_URL = '/auth'


class HerokuConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    PORT = os.environ.get('PORT', 4000)
    DEBUG = True


class Local(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../app.sqlite'
    # SQLALCHEMY_DATABASE_URI = 'postgres://homeautomation@localhost/homeautomation'
    DEBUG = True


class Travis(Config):
    SQLALCHEMY_DATABASE_URI = 'postgres://postgres@localhost/travis_ci_test'
    DEBUG = True


class Kubernetes(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    PORT = os.environ.get('PORT', 4000)
    DEBUG = True
