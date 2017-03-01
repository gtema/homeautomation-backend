DEBUG = True
# SQLAlchemy settings
SQLALCHEMY_DATABASE_URI = 'sqlite:///../app.sqlite'

CACHE_TYPE = 'simple'

# Security Settings
# https://pythonhosted.org/Flask-Security/configuration.html

SECURITY_CONFIRMABLE           = True
SECURITY_TRACKABLE             = True
SECURITY_REGISTERABLE          = True
SECURITY_RECOVERABLE           = True
# SECURITY_PASSWORD_HASH         = 'plaintext'
SECURITY_PASSWORD_HASH         = 'sha512_crypt'
SECURITY_PASSWORD_SALT         = 'add_salt'
SQLALCHEMY_TRACK_MODIFICATIONS = False
