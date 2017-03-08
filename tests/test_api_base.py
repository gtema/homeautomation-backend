import unittest
import os
import sys
import werkzeug

from flask import json, request
from flask_marshmallow import Marshmallow
from marshmallow import fields

from homeautomation import create_app
from homeautomation.models import db, BaseCrud
from homeautomation.api_v1.resources.base import BaseResource

ma = Marshmallow()

__all__ = ["BaseResourceTestCase"]

"""Base objects test: BaseCrud, BaseResource
"""


class TestModel(db.Model, BaseCrud):
    __tablename__ = "base_test_model"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    parent_id = db.Column(db.Integer)
    name = db.Column(db.String(255), nullable=False)


class TestSchema(ma.ModelSchema):
    class Meta:
        # fields=('id', 'parent_id', 'name')
        model = TestModel

    id = fields.Int(dump_only=True)
    parent_id = fields.Int()
    name = fields.Str()


class BaseResourceTestCase(unittest.TestCase):

    class testConfig():
        # Setup an in-memory SQLite DB, create schema
        TESTING = True
        SQLALCHEMY_DATABASE_URI = 'sqlite://'
        SECURITY_PASSWORD_HASH = 'plaintext'
        SECURITY_PASSWORD_SALT = '2'
        SEC_AUTH_URL_RULE = '/auth'
        DEBUG = False

    class TestResourceMulti(BaseResource):
        def __init__(self):
            super().__init__(TestModel,
                             TestSchema(many=True),
                             TestModel.name)

        def get(self, q):
            return super().get(q)

        def put(self, q):
            return super().put(q)

        def post(self):
            return super().post()

        def delete(self, q):
            return super().delete(q)

    class TestResourceSingle(BaseResource):
        def __init__(self):
            super().__init__(TestModel,
                             TestSchema(many=False),
                             TestModel.id)

        def get(self, q):
            return super().get(q)

        def put(self, q):
            return super().put(q)

        def post(self):
            return super().post()

        def delete(self, q):
            return super().delete(q)

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
            db.session.query(TestModel).delete()
            db.session.commit()

    def tearDown(self):
        """
        tearDown
        """
        with self.app.app_context():
            db.session.remove()

    def testSinglePOST(self):
        'add new entity'
        res = self.TestResourceSingle()

        test_obj = {
            'id': 1,
            'name': 't1',
            'parent_id': 0,
        }

        with self.app.test_request_context('/',
                                           method='POST',
                                           data=json.dumps(test_obj),
                                           content_type='application/json'):
            rv = res.dispatch_request()
            self.assertEqual(201, rv.status_code)

            ret = json.loads(rv.data)

            self.assertEqual(test_obj['parent_id'],
                             ret['parent_id'], 'parent_id of test entity')
            self.assertEqual(test_obj['name'],
                             ret['name'], 'name of test entity')

    def testSinglePOSTNoInput(self):
        'add new entity with no input'
        res = self.TestResourceSingle()

        test_obj = {}

        with self.app.test_request_context('/',
                                           method='POST',
                                           data=json.dumps(test_obj),
                                           content_type='application/json'):
            rv = res.dispatch_request()
            self.assertEqual(400, rv.status_code)

    def testSinglePOSTWrongSchema(self):
        'add new entity with wrong data'
        res = self.TestResourceSingle()

        test_obj = {'id': 'test', 'parent_id': 'ccc'}

        with self.app.test_request_context('/',
                                           method='POST',
                                           data=json.dumps(test_obj),
                                           content_type='application/json'):
            rv = res.dispatch_request()
            self.assertEqual(422, rv.status_code)

    def testSingleGETOK(self):
        'get existing entity'
        res = self.TestResourceSingle()

        test_obj = {
            'id': 1,
            'name': 't1',
            'parent_id': 1,
        }

        with self.app.app_context():
            # expand dict and insert
            db.session.add(TestModel(**test_obj))

            db.session.commit()
        with self.app.test_request_context('/',
                                           method='GET'):
            rv = res.dispatch_request(1)

            self.assertEqual(200, rv.status_code)

            ret = json.loads(rv.data)

            self.assertEqual(test_obj['id'], ret['id'],
                             'id of test entity')
            self.assertEqual(test_obj['parent_id'], ret['parent_id'],
                             'parent_id of test entity')
            self.assertEqual(test_obj['name'], ret['name'],
                             'name of test entity')

    def testSingleGETMultiByName(self):
        'get non existing entity'
        res = self.TestResourceMulti()

        objects = (
            (1, 20, 'test1'),
            (2, 20, 'test2'),
            (3, 20, 'test3'),
            (4, 20, 'Testing'),
            (5, 22, 'shoul not come'),
        )

        import re

        expected = []

        for (id, parent_id, name) in objects:
            if re.search('test', name, re.IGNORECASE):
                expected.append({
                                'id': id,
                                'parent_id': parent_id,
                                'name': name
                                })

        with self.app.app_context():
            for (xid, pid, name) in objects:
                db.session.add(TestModel(id=xid,
                                         parent_id=pid,
                                         name=name))

            db.session.commit()

        with self.app.test_request_context('/',
                                           method='GET'):
            rv = res.get_by_name('test')
            ret = json.loads(rv.data)
            self.assertListEqual(expected, ret)

    def testSingleGETOK(self):
        'get existing entity'
        res = self.TestResourceSingle()

        test_obj = {
            'id': 1,
            'name': 't1',
            'parent_id': 1,
        }

        with self.app.app_context():
            # expand dict and insert
            db.session.add(TestModel(**test_obj))

            db.session.commit()
        with self.app.test_request_context('/',
                                           method='GET'):
            rv = res.dispatch_request(1)

            self.assertEqual(200, rv.status_code)

            ret = json.loads(rv.data)

            self.assertEqual(test_obj['id'], ret['id'],
                             'id of test entity')
            self.assertEqual(test_obj['parent_id'], ret['parent_id'],
                             'parent_id of test entity')
            self.assertEqual(test_obj['name'], ret['name'],
                             'name of test entity')

    def testSinglePUT(self):
        'modify existing entity'
        res = self.TestResourceSingle()

        test_obj = {
            'id': 1,
            'name': 't1',
            'parent_id': 1,
        }

        with self.app.app_context():
            # expand dict and insert
            db.session.add(TestModel(**test_obj))
            db.session.commit()

        with self.app.test_request_context('/',
                                           method='PUT',
                                           data=json.dumps(test_obj),
                                           content_type='application/json'):
            rv = res.dispatch_request(1)

            self.assertEqual(200, rv.status_code)

            ret = json.loads(rv.data)

            self.assertEqual(test_obj['parent_id'], ret['id'],
                             'id of test entity')
            self.assertEqual(test_obj['parent_id'],
                             ret['parent_id'], 'parent_id of test entity')
            self.assertEqual(test_obj['name'],
                             ret['name'], 'name of test entity')

    def testSinglePUTNonExisting(self):
        'modify nonexisting entity'
        res = self.TestResourceSingle()

        test_obj = {
            'id': 2,
            'name': 't1',
            'parent_id': 1,
        }

        with self.app.app_context():
            db.session.query(TestModel).delete()
            db.session.commit()

        with self.app.test_request_context('/',
                                           method='PUT',
                                           data=json.dumps(test_obj),
                                           content_type='application/json'):
            # ensure 404 is raised
            with self.assertRaises(werkzeug.exceptions.NotFound) as e:
                rv = res.dispatch_request(2)

    def testSingleDELETE(self):
        'delete existing entity'
        res = self.TestResourceSingle()

        test_obj = {
            'id': 1,
            'name': 't1',
            'parent_id': 1,
        }

        with self.app.app_context():
            db.session.add(TestModel(**test_obj))
            db.session.add(TestModel(id=2, parent_id=3, name='fff'))
            db.session.commit()

        with self.app.test_request_context('/',
                                           method='DELETE'):
            rv = res.dispatch_request(test_obj['id'])

            self.assertEqual(204, rv.status_code)

        with self.app.app_context():
            items = db.session.query(TestModel)
            self.assertIsNone(items.filter(
                TestModel.id == test_obj['id']).first())
            self.assertIsNotNone(items.filter(
                TestModel.id == 2).first())

    def testSingleDELETENonExisting(self):
        'delete existing entity'
        res = self.TestResourceSingle()

        with self.app.app_context():
            db.session.query(TestModel).delete()
            db.session.commit()

        with self.app.test_request_context('/',
                                           method='DELETE'):
            # ensure 404 is raised
            with self.assertRaises(werkzeug.exceptions.NotFound) as e:
                rv = res.dispatch_request(2)

    # TODO: add more Multi model tests
