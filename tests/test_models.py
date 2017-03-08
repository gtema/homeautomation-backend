import unittest
import os

from homeautomation import create_app
from homeautomation.models import db,\
    StockProductCategory, StockProductItem, StockProduct

"""Models tests
"""


class ModelsTestCase(unittest.TestCase):
    """ Basic tests for the ORM - virtual fields, constraints, etc.
    """

    class testConfig():
        # Setup an in-memory SQLite DB, create schema
        TESTING = True
        SQLALCHEMY_DATABASE_URI = 'sqlite://'
        SECURITY_PASSWORD_HASH = 'plaintext'
        SECURITY_PASSWORD_SALT = '2'
        SEC_AUTH_URL_RULE = '/auth'
        DEBUG = False

    @classmethod
    def setUpClass(cls):
        """
        test setup class: instantiate app with modified config, initialize db
        """
        # load config given in APP_SETTINGS or use testConfig object
        config = os.environ.get('APP_SETTINGS')
        if config is None:
            config = __class__.testConfig

        cls.app = create_app(config)
        cls.test_client = cls.app.test_client()
        # db.init_app(app)

        with cls.app.app_context():
            db.drop_all()
            db.create_all()
            db.session.commit()

    @classmethod
    def tearDownClass(cls):
        with cls.app.app_context():
            db.drop_all()

    def setUp(self):
        """
        Cleanup tables
        """
        # with an app context create db schema
        with self.app.app_context():
            db.session.query(StockProductItem).delete()
            db.session.query(StockProduct).delete()
            db.session.query(StockProductCategory).delete()
            db.session.commit()

    def tearDown(self):
        """
        tearDown
        """
        with self.app.app_context():
            db.session.remove()

    category_data = [
        {'id': 0, 'parent_id': None, 'name': 'root'},
        {'id': 1, 'parent_id': 0, 'name': 'r1'},
        {'id': 2, 'parent_id': 0, 'name': 'r2'},
    ]

    product_data = [
        {'id': 1, 'category_id': 1, 'name': 'r1-p1', 'sum_amounts': True},
        {'id': 2, 'category_id': 1, 'name': 'r1-p2', 'sum_amounts': False},
        {'id': 3, 'category_id': 2, 'name': 'r2-p1', 'sum_amounts': True},
    ]

    product_item_data = [
        {'id': 1, 'product_id': 1, 'amount': 1,
            'is_started': True, 'is_disposed': True},
        {'id': 2, 'product_id': 1, 'amount': 3,
            'is_started': False, 'is_disposed': False},
        {'id': 3, 'product_id': 1, 'amount': 3,
            'is_started': True, 'is_disposed': False},
        {'id': 4, 'product_id': 2, 'amount': 1,
            'is_started': False, 'is_disposed': False},
        {'id': 5, 'product_id': 2, 'amount': 4,
            'is_started': False, 'is_disposed': False},
        {'id': 6, 'product_id': 3, 'amount': 0,
            'is_started': False, 'is_disposed': False},
    ]

    def testModelCategory(self):
        'test categories'
        with self.app.app_context():
            for rec in self.category_data:
                db.session.add(StockProductCategory(**rec))

            items = db.session.query(StockProductCategory)
            self.assertIsNotNone(
                items.filter(
                    StockProductCategory.id == self.category_data[0]['id'])
                .first(),
                'root is present in the db')
            self.assertIsNotNone(
                items.filter(
                    StockProductCategory.id == self.category_data[1]['id'])
                .first(),
                'r1 is present in the db')
            items\
                .filter(StockProductCategory.id ==
                        self.category_data[1]['id'])\
                .delete()
            self.assertIsNotNone(
                items.filter(
                    StockProductCategory.id == self.category_data[0]['id'])
                .first(),
                'root is still present in the db')
            items\
                .filter(StockProductCategory.id ==
                        self.category_data[0]['id'])\
                .delete()

    def testModelProduct(self):
        'test products'
        with self.app.app_context():
            for rec in self.category_data:
                db.session.add(StockProductCategory(**rec))
            for rec in self.product_data:
                db.session.add(StockProduct(**rec))
            for rec in self.product_item_data:
                db.session.add(StockProductItem(**rec))

            categories = db.session.query(StockProductCategory)
            products = db.session.query(StockProduct)
            items = db.session.query(StockProductItem)

            p1 = products.filter(StockProduct.name == 'r1-p1').first()
            p2 = products.filter(StockProduct.name == 'r1-p2').first()
            p3 = products.filter(StockProduct.name == 'r2-p1').first()

            self.assertEqual(6, p1.amount,
                             'amount=sum of amounts of not disposed items')
            self.assertEqual(3, p1.first_started_id,
                             'first_started_id is id of open item '
                             'with earliest expiry')

            self.assertEqual(2, p2.amount,
                             'amount=sum of amounts of not disposed items')
            self.assertEqual(None, p2.first_started_id,
                             'no open items')

    def testModelProductItems(self):
        'test product items'
        with self.app.app_context():
            for rec in self.category_data:
                db.session.add(StockProductCategory(**rec))
            for rec in self.product_data:
                db.session.add(StockProduct(**rec))
            for rec in self.product_item_data:
                db.session.add(StockProductItem(**rec))

            categories = db.session.query(StockProductCategory)
            products = db.session.query(StockProduct)
            items = db.session.query(StockProductItem)

            pi1 = items.filter(StockProductItem.id == 1).first()
            pi2 = items.filter(StockProductItem.id == 3).first()
            pi3 = items.filter(StockProductItem.id == 6).first()

            self.assertEqual(False, pi1.is_valid,
                             'disposed item is not valid')
            self.assertEqual(True, pi2.is_valid,
                             'item with amount> and not is_disposed is valid')
            self.assertEqual(False, pi3.is_valid,
                             'item with amount = 0 is not valid')
