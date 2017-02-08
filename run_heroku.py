from homeautomation import create_app
import os


class herokuConfig(object):
    # Setup an in-memory SQLite DB, create schema
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

app = create_app(herokuConfig)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
