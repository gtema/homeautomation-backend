from flask import abort

from homeautomation.models import StockProductCategory
from homeautomation.schemas import CategorySchema

from .base import BaseResource


class StockCategories(BaseResource):
    '''
    Api to return all subCategorys of the given Category (or root, parent_id=0)
    '''
    # decorators = [jwt_required()]

    def __init__(self):
        super().__init__(StockProductCategory,
                         CategorySchema(many=True),
                         StockProductCategory.parent_id)

    def get(self, id=None):
        '''
        GET method to return all subCategorys of the given Category
        (parent_id=<CATEGORY_ID:0>)
        or all available categories
        '''
        return super().get(id)

    def post(self, id=0):
        return abort(405)

    def put(self, id=0):
        return abort(405)

    def delete(self, id=0):
        return abort(405)


class StockCategory(BaseResource):
    '''
    Api to process single Category by it's ID
    '''
    # decorators = [jwt_required()]

    def __init__(self):
        super().__init__(StockProductCategory,
                         CategorySchema(),
                         StockProductCategory.id)

    def get(self, id=0):
        '''
        GET method to return the single Product by ID
        '''
        return super().get(id)

    def put(self, id):
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
        DELETE method to delete Category
        '''
        return super().delete(id)
