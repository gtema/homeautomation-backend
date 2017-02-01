from flask import jsonify, make_response, abort
from flask_restful import Resource
from flask_jwt import jwt_required

from homeautomation.models import StockProduct
from homeautomation.schemas import ProductSchema

from .base import BaseResource


class StockCategoryProducts(BaseResource):
    '''
    Api to return all subCategorys of the given Category (or root, parent_id=0)
    '''
    decorators = [jwt_required()]

    def __init__(self):
        super().__init__(StockProduct,
                         ProductSchema(many=True),
                         StockProduct.category_id)

    def get(self, id):
        return super().get(id)

    def post(self, id=0):
        return abort(405)

    def put(self, id=0):
        return abort(405)

    def delete(self, id=0):
        return abort(405)


class StockCategoryProduct(BaseResource):
    '''
    Api to process single Category by it's ID
    '''
    decorators = [jwt_required()]

    def __init__(self):
        super().__init__(StockProduct, ProductSchema(), StockProduct.id)

    def get(self, id=0):
        '''
        GET method to return the single Product by ID
        '''
        if id == 0:
            return make_response(
                    jsonify({
                     'message': 'Product GET without ID is not allowed'
                    }),
                    422)
        else:
            return super().get(id)

    def put(self, id=0):
        '''
        PUT method to modify the single Product by ID
        '''
        return super().put(id)

    def post(self):
        '''
        POST method to add new entity
        '''
        return super().post()

    def delete(self, id=0):
        '''
        DELETE method to drop product
        '''
        return super().delete(id)
