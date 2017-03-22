import os


def application(environ, start_response):
    for key in ['FLASKR_SETTINGS', ]:
        os.environ[key] = environ.get(key, '')
    from homeautomation import create_app as _application

    return _application().wsgi_app(environ, start_response)
