import unittest
import os
import homeautomation
from homeautomation.models import User
#from StockManager import app, db
from flask import json

TEST_DB = 'test_db.sqlite'

API_URL_PREFIX = "/api/v0/stock"

def get_auth():
    return "?api_key=2"

def dictMinus(dct, val):
    copy = dct.copy()
    del copy[val]
    return copy
   
class StockManagerApiTestCase(unittest.TestCase):

    def setUp(self):
        self.basedir = os.path.abspath(os.path.dirname(__file__))
        self.db_fd = os.path.join(self.basedir, TEST_DB)
        homeautomation.app.config['TESTING'] = True
        homeautomation.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + self.db_fd
        homeautomation.app.config['WTF_CSRF_ENABLED'] = False
        self.app = homeautomation.app.test_client()
        with homeautomation.app.app_context():
             homeautomation.db.create_all()
        user = User(username='test', password='test')
        homeautomation.db.session.add(user)
        homeautomation.db.session.commit()

    def tearDown(self):
#        os.close(app.config['SQLALCHEMY_DATABASE_URI'])
        os.unlink(self.db_fd)
    
    category1 = dict(
            name='root1', 
            parent_id = 0
            )            

    category2 = dict(
            name='root2', 
            parent_id = 0
            ) 
    
    product1 = dict(
        name = 'tp1', 
#        category_id = category1['id'], 
        )

    def __check_success(self, src,  target):
        assert 200 == target['status']
        if 'id' in src.keys():
            self.assertDictEqual(src,  target['obj'],  'Returned entry is expected one')
        else:
            self.assertDictEqual(src,  dictMinus(target['obj'],  'id'),  'Returned entry is expected one')
    
    def __add_entity(self,  type,  entity,  expected_rc = 200):
        'add entity'
        rv = self.app.post(API_URL_PREFIX + "/" + type + get_auth(),  data=json.dumps(entity),  content_type = 'application/json')
        ret = json.loads(rv.data)
        assert expected_rc == rv.status_code
        return {'status' : rv.status_code,  'obj' : ret}

    def __del_entity(self,  type,  id = 0,  expected_rc = 200):
        'delete entity'
        id_selector = "/" + repr(id) #if id else ''
        rv = self.app.delete(API_URL_PREFIX + "/" + type + id_selector + get_auth())
        ret = json.loads(rv.data)
        assert expected_rc == rv.status_code
        return {'status' : rv.status_code,  'obj' : ret}

    def __change_entity(self,  type,  original_id,  entity,  expected_rc = 200):
        'modify entity'
        rv = self.app.put(API_URL_PREFIX + "/" + type + "/" + repr(original_id) + get_auth(),  data=json.dumps(entity),  content_type = 'application/json')
        ret = json.loads(rv.data)
        assert expected_rc == rv.status_code
        return {'status' : rv.status_code,  'obj' : ret}

    def __get_entity(self,  type,  id,  expected_rc = 200):
        'delete entity'
        id_selector = "/" + repr(id) if id else ''
        rv = self.app.get(API_URL_PREFIX + "/" + type + id_selector + get_auth())
        ret = json.loads(rv.data)
        assert expected_rc == rv.status_code
        return {'status' : rv.status_code,  'obj' : ret}

    def test_categorys_post(self):
        '''no input test'''
        ret = self.__add_entity('category',  dict(),  400)
        assert 'No input' == ret['obj']['message']
        
        '''no name given'''
        ret = self.__add_entity('category',  dict(parent_id=1),  422)
        assert 'Missing data for required field.' in ret['obj']['name']

        '''wrong name, missing parent_id'''
        ret = self.__add_entity('category',  dict(name=1),  422)
        assert 'Not a valid string.' in ret['obj']['name']
#        assert 'Missing data for required field.' in ret['parent_id']

        'add entity'
        ret = self.__add_entity('category',  self.category1)
        self.__check_success(self.category1,  ret)
        
        'cleanup entity'
        self.__del_entity('category',  ret['obj']['id'])

    def test_category_get(self):
        'create root'
        ret = self.__add_entity('category',  self.category1)
#        self.__check_success(self.category1,  ret)
        self.category1['id'] = ret['obj']['id']

        'add another root'
        ret = self.__add_entity('category',  self.category2)
#        self.__check_success(self.category2,  ret)
        self.category2['id'] = ret['obj']['id']

        'ensure direct request'
        ret = self.__get_entity('category',  self.category1['id'])
        self.assertDictEqual(self.category1,  ret['obj'],  'Returned entry is expected one')

        'ensure default category request'
        ret = self.__get_entity('categories',  False)
        assert 2 == len(ret['obj'])
        self.assertDictEqual(self.category1,  ret['obj'][0],  'Returned entry is expected one')
        self.assertDictEqual(self.category2,  ret['obj'][1],  'Returned entry is expected one')

    def test_category_put(self):
        'add new test entity'
        test_entity = self.category1.copy()
        del test_entity['id']

        ret = self.__add_entity('category',  test_entity)
#        self.__check_success(test_entity,  ret)
        test_entity['id'] = ret['obj']['id']

        'modify entity object'
        test_entity['name'] = 'new name'
        
        'update category1 name'
        ret = self.__change_entity('category',  test_entity['id'],  test_entity)
        self.__check_success(test_entity,  ret)

        'ensure GET returns the same'
        ret = self.__get_entity('category',  test_entity['id'])
        self.__check_success(test_entity,  ret)
#        self.assertDictEqual(test_entity,  ret['obj'],  'Returned entry is expected one')
        
        'cleanup'
        ret = self.__del_entity('category',  test_entity['id'])
    
    def test_category_del(self):
        ret = self.__add_entity('category',  self.category1)
#        self.__check_success(self.category1,  ret)
        self.category1['id'] = ret['obj']['id']
        
        'delete by id'
        ret = self.__del_entity('category',  self.category1['id'],  200)

        'delete with no id'
        ret = self.__del_entity('category',  0,  404)

        'delete not existing'
        ret = self.__del_entity('category',  10099,  404)
    
    def test_product_post(self):
        ret = self.__add_entity('category',  self.category1)
        self.product1['category_id'] = ret['obj']['id']
        ret = self.__add_entity('product',  self.product1)
        self.product1['id'] = ret['obj']['id']
        self.__del_entity('product',  ret['obj']['id'])
        self.__del_entity('category',  self.product1['id'] )
        
    def test_product_get(self):
        ret = self.__add_entity('category',  self.category1)
        self.product1['category_id'] = ret['obj']['id']
        ret = self.__add_entity('product',  self.product1)
        self.product1['id'] = ret['obj']['id']
        
        product_item = dict(
            product_id = self.product1['id'], 
            amount = 2, 
            is_started = True
            )
        
        ret = self.__add_entity('product_item',  product_item)
        print ("product_item ",  ret['obj']['id'])
        
        ret = self.__get_entity('product',  self.product1['id'] )
        print ("returning xxx ",  ret['obj'])
        assert False
        self.__del_entity('category',  self.product1['id'] )
        
    def test_product_put(self):
        test_entity = self.product1.copy()
        ret = self.__add_entity('category',  self.category1)
        test_entity ['category_id'] = ret['obj']['id']
        ret = self.__add_entity('product',  test_entity )
        test_entity ['id'] = ret['obj']['id']
        test_entity['name'] = 'new name'

        ret = self.__change_entity('product',  test_entity ['id'],  test_entity)
        ret1 = self.__get_entity('product',  test_entity['id'])
        self.assertDictEqual(ret['obj'],  ret1['obj'])

        ret = self.__get_entity('product',  test_entity['id'] )
        self.__del_entity('category',  test_entity['id'] )
        
    def test_product_del(self):
        test_entity = self.product1.copy()
        ret = self.__add_entity('category',  self.category1)
        test_entity ['category_id'] = ret['obj']['id']
        ret = self.__add_entity('product',  test_entity )
        test_entity ['id'] = ret['obj']['id']

        ret = self.__get_entity('product',  test_entity['id'] )
        self.__del_entity('category',  test_entity['id'] )

if __name__ == '__main__':
    unittest.main()
