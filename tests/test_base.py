import unittest
import os
from flask import json

from homeautomation import create_app
from homeautomation.models import db


class testConfig(object):
    # Setup an in-memory SQLite DB, create schema
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    DEBUG = True
    XXX = "here I am"


class GeneralAppTestCase(unittest.TestCase):

    def testApplicationFactory(self):
        app=create_app()
        assert app

    def testConfigOverride(self):
        app = create_app(testConfig)
        assert testConfig.XXX == app.config['XXX']

    def testDbInitialization(self):
        app = create_app(testConfig)
        with app.app_context():
            db.drop_all()
            db.create_all()
