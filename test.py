import unittest
import os
import homeautomation
from homeautomation.models import User
from homeautomation import app, db

#from api_test import StockManagerApiTestCase

TEST_DB = 'test_db.sqlite'

# class FlaskrTestCase(unittest.TestCase):
#
#     def setUp(self):
#         self.db_fd, StockManager.app.config['DATABASE'] = tempfile.mkstemp()
#         StockManager.app.config['TESTING'] = True
#         self.app = StockManager.app.test_client()
#         with StockManager.app.app_context():
#             StockManager.init_db()
#
#     def tearDown(self):
#             os.close(self.db_fd)
#             os.unlink(StockManager.app.config['DATABASE'])


class StockManagerTestCase(unittest.TestCase):

    def setUp(self):
        self.basedir = os.path.abspath(os.path.dirname(__file__))
        self.db_fd = os.path.join(self.basedir, TEST_DB)
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
            self.db_fd
#        self.db_fd, StockManager.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://' + tempfile.mkstemp()

        homeautomation.app.config['WTF_CSRF_ENABLED'] = False
        self.app = homeautomation.app.test_client()
        with homeautomation.app.app_context():
             db.create_all()
        user = User(username='test', password='test')
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
#        os.close(app.config['SQLALCHEMY_DATABASE_URI'])
        os.unlink(self.db_fd)

    def login(self, username, password):
        return self.app.post('/login', data=dict(username=username, password=password, csrf_token='rrr'), follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    def test_login_logout(self):
        rv = self.login('test', 'test')
        assert b'Logged in successfully' in rv.data
        rv = self.logout()
        assert b'Logged out successfully' in rv.data
        rv = self.login('adminx', 'default')
        assert b'Invalid username' in rv.data
        rv = self.login('admin', 'defaultx')
        assert b'Invalid password' in rv.data


if __name__ == '__main__':
    unittest.main()
