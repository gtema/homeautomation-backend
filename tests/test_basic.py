import unittest

from homeautomation import create_app
from homeautomation.models import db


class GeneralAppTestCase(unittest.TestCase):

    class testConfig():
        # Setup an in-memory SQLite DB, create schema
        TESTING = True
        SQLALCHEMY_DATABASE_URI = 'sqlite://'
        DEBUG = True
        XXX = "here I am"

    def testApplicationFactory(self):
        app = create_app()
        self.assertIsNotNone(app)

    def testConfigOverride(self):
        app = create_app(self.testConfig)
        self.assertEqual(self.testConfig.XXX, app.config['XXX'])

    def testDbInitialization(self):
        app = create_app(self.testConfig)
        with app.app_context():
            db.drop_all()
            db.create_all()
