DEBUG = True
# SQLAlchemy settings
SQLALCHEMY_DATABASE_URI = 'sqlite:///../app.sqlite'

CACHE_TYPE = 'simple'

# Security Settings
# https://pythonhosted.org/Flask-Security/configuration.html
# https://pythonhosted.org/Flask-JWT/
# JWT_EXPIRATION_DELTA           = timedelta(days=30)
JWT_AUTH_URL_RULE              = '/api/v0/auth'
JWT_AUTH_USERNAME_KEY          = 'username'
JWT_AUTH_PASSWORD_KEY          = 'password'
SECURITY_CONFIRMABLE           = True
SECURITY_TRACKABLE             = True
SECURITY_REGISTERABLE          = True
SECURITY_RECOVERABLE           = True
# SECURITY_PASSWORD_HASH         = 'plaintext'
SECURITY_PASSWORD_HASH         = 'sha512_crypt'
SECURITY_PASSWORD_SALT         = 'add_salt'
SQLALCHEMY_TRACK_MODIFICATIONS = False
