import unittest
import os
from flask import json
from flask_security.utils import encrypt_password

from homeautomation.models import user_datastore,\
    StockProductCategory, StockProductItem, StockProduct
from homeautomation import create_app
from homeautomation.models import db


"""Api tests
"""

API_URL_PREFIX = "/api/v0/stock"


class testConfig(object):
    # Setup an in-memory SQLite DB, create schema
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    SECURITY_PASSWORD_HASH = 'plaintext'
    SECURITY_PASSWORD_SALT = '2'
    SEC_AUTH_URL_RULE = '/auth'
    DEBUG = False


class ApiTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        test setup class: instantiate app with modified config, initialize db
        """
        # load config given in APP_SETTINGS or use testConfig object
        config = os.environ.get('APP_SETTINGS')
        if config is None:
            config = testConfig

        cls.app = create_app(config)
        cls.test_client = cls.app.test_client()

        with cls.app.app_context():
            db.drop_all()
            db.create_all()
            user_datastore.create_user(username='t1',
                                       password=encrypt_password('plaintext'),
                                       api_key='adglhve')
            db.session.commit()

    def setUp(self):
        """
        Cleanup tables
        """
        # with an app context create db schema
        with self.app.app_context():
            pass
            # db.drop_all()
            # db.create_all()
            db.session.query(StockProductItem).delete()
            db.session.query(StockProduct).delete()
            db.session.query(StockProductCategory).delete()
            db.session.add(StockProductCategory(id=0,
                                                parent_id=None,
                                                name='_root'))
            db.session.commit()

    def tearDown(self):
        """
        tearDown
        """
        with self.app.app_context():
            db.session.remove()

    def login(self):
        """
        login method to issue a token request
        """
        self.auth = json.loads(self.test_client.post(
            self.app.config.get('SEC_LOGIN_URL'),
            data=json.dumps(
                dict(username='t1', password='plaintext')),
            content_type='application/json').data)

    def buildRequestHeader(self):
        return dict(Authorization='API_KEY ' + self.auth['api_key'])

    category1 = dict(
        name='root1',
        parent_id=0,
        prio=0
    )

    category2 = dict(
        name='root2',
        parent_id=0,
        prio=0
    )

    product1 = dict(
        name='tp1'
    )

    def __check_success(self, src, target):
        """
        Internal method to ensure call was successfull
        """
        self.assertEqual(200, target['status'], 'return code success')
        if 'id' in src.keys():
            self.assertDictEqual(src,
                                 target['obj'],
                                 'Returned entry is expected one')
        else:
            self.assertDictEqual(src,
                                 dictMinus(target['obj'], 'id'),
                                 'Returned entry is expected one')

    def __add_entity(self, type, entity, expected_rc=201):
        """
        Internal add entity
        """
        url = '{:s}/{:s}'.format(API_URL_PREFIX, type)
        rv = self.test_client.post(url,
                                   data=json.dumps(entity),
                                   content_type='application/json',
                                   headers=self.buildRequestHeader()
                                   )
        ret = json.loads(rv.data)

        self.assertEqual(expected_rc,
                         rv.status_code,
                         'return code as expected')
        return {'status': rv.status_code, 'obj': ret}

    def __del_entity(self, type, id=0, expected_rc=204):
        """
        Internal delete entity
        """
        id_selector = "/" + repr(id)
        url = '{:s}/{:s}{:s}'.format(API_URL_PREFIX, type, id_selector)
        rv = self.test_client.delete(url,
                                     headers=self.buildRequestHeader()
                                     )
        self.assertEqual(expected_rc,
                         rv.status_code,
                         'return code as expected')
        return {'status': rv.status_code, 'obj': None}

    def __change_entity(self, type, original_id, entity, expected_rc=200):
        """
        Internal modify entity
        """
        url = '{:s}/{:s}/{:d}'.format(API_URL_PREFIX, type, original_id)
        rv = self.test_client.put(url,
                                  data=json.dumps(entity),
                                  content_type='application/json',
                                  headers=self.buildRequestHeader()
                                  )
        ret = json.loads(rv.data)
        self.assertEqual(expected_rc,
                         rv.status_code,
                         'return code as expected')
        return {'status': rv.status_code, 'obj': ret}

    def __get_entity(self, type, id, expected_rc=200):
        """
        Internal GET entity
        """
        id_selector = "/" + repr(id) if id else ''
        url = '{:s}/{:s}{:s}'.format(API_URL_PREFIX, type, id_selector)
        rv = self.test_client.get(url,
                                  headers=self.buildRequestHeader())
        ret = json.loads(rv.data)
        self.assertEqual(expected_rc,
                         rv.status_code,
                         'return code as expected')
        return {'status': rv.status_code, 'obj': ret}

    def test_categorys_post(self):
        """no input test"""
        self.login()
        ret = self.__add_entity('category', dict(), 400)
        self.assertEqual('No input', ret['obj']['message'], 'No input return')

        """no name given"""
        ret = self.__add_entity('category', dict(parent_id=1), 422)
        self.assertEqual(True,
                         'Missing data for required field.'
                         in ret['obj']['name'],
                         'error contains "missing data"')

        """wrong name, missing parent_id"""
        ret = self.__add_entity('category', dict(name=1), 422)
        self.assertEqual(True,
                         'Not a valid string.' in ret['obj']['name'],
                         'error contains "not a valid string"')
#        assert 'Missing data for required field.' in ret['parent_id']

        'add entity'
        ret = self.__add_entity('category', self.category1)

    def test_category_get(self):
        'create root'
        self.login()
        ret = self.__add_entity('category', self.category1)
        self.category1['id'] = ret['obj']['id']

        'add another root'
        ret = self.__add_entity('category', self.category2)
        self.category2['id'] = ret['obj']['id']

        'ensure direct request'
        ret = self.__get_entity('category', self.category1['id'])
        self.assertDictEqual(self.category1,
                             ret['obj'],
                             'Returned entry is expected one')

        'ensure default category request'
        ret = self.__get_entity('categories', False)

        self.assertEqual(2, len(ret['obj']), 'only 2 categories')

        self.assertDictEqual(self.category1,
                             ret['obj'][0],
                             'Returned entry is expected one')
        self.assertDictEqual(self.category2,
                             ret['obj'][1],
                             'Returned entry is expected one')

    def test_category_put(self):
        'add new test entity'
        self.login()
        test_entity = self.category1.copy()
        del test_entity['id']

        ret = self.__add_entity('category', test_entity)
        test_entity['id'] = ret['obj']['id']

        'modify entity object'
        test_entity['name'] = 'new name'

        'update category1 name'
        ret = self.__change_entity('category', test_entity['id'], test_entity)
        self.__check_success(test_entity, ret)

        'ensure GET returns the same'
        ret = self.__get_entity('category', test_entity['id'])
        self.__check_success(test_entity, ret)

    def test_category_del(self):
        ' test delete category'
        self.login()

        ret = self.__add_entity('category', self.category1)
        self.category1['id'] = ret['obj']['id']

        'delete by id'
        ret = self.__del_entity('category', self.category1['id'], 204)

        'delete with no id'
        ret = self.__del_entity('category', 0, 405)

        'delete not existing'
        ret = self.__del_entity('category', 10099, 404)

    def test_product_post(self):
        'Create new product'
        self.login()

        'Create parent category for consistency'
        ret = self.__add_entity('category', self.category1)
        self.product1['category_id'] = ret['obj']['id']

        'Create product'
        ret = self.__add_entity('product', self.product1)
        self.product1['id'] = ret['obj']['id']

    def test_product_get(self):
        'Get products and items'
        self.login()

        'create parent category'
        ret = self.__add_entity('category', self.category1)
        self.product1['category_id'] = ret['obj']['id']

        'create product'
        ret = self.__add_entity('product', self.product1)
        self.product1['id'] = ret['obj']['id']

        product_item = dict(
            product_id=self.product1['id'],
            amount=2,
            is_started=True
        )

        'add product_item'
        ret = self.__add_entity('product_item', product_item)
        product_item['id'] = ret['obj']['id']

        'check product'
        ret = self.__get_entity('product', self.product1['id'])

        'check product_item'
        ret = self.__get_entity('product_item', product_item['id'])

    def test_product_put(self):
        'modify products'
        self.login()
        test_entity = self.product1.copy()
        'add parent category'
        ret = self.__add_entity('category', self.category1)
        test_entity['category_id'] = ret['obj']['id']

        'add product'
        ret = self.__add_entity('product', test_entity)
        test_entity['id'] = ret['obj']['id']
        # test_entity['category_id'] = ret['obj']['category_id']
        test_entity['name'] = 'new name'

        'modify product'
        ret = self.__change_entity('product', test_entity['id'], test_entity)

        'check entity'
        ret1 = self.__get_entity('product', test_entity['id'])
        self.assertDictEqual(ret['obj'], ret1['obj'])

    def test_product_del(self):
        'delete products'
        self.login()
        test_entity = self.product1.copy()
        'create parent category'
        ret = self.__add_entity('category', self.category1)
        test_entity['category_id'] = ret['obj']['id']

        'create product'
        ret = self.__add_entity('product', test_entity)
        test_entity['id'] = ret['obj']['id']

        self.__del_entity('product', test_entity['id'])
