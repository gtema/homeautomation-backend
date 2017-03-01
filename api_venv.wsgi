activate_this = '/var/www/homeautomation/venv/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))


from homeautomation import app as application
