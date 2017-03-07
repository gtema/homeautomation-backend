from flask import abort, current_app

from homeautomation.models import StockProductCategory
from homeautomation.schemas import CategorySchema

from .base import BaseResource


class StockCategories(BaseResource):
    """
    Api to return all subCategorys of the given Category (or root, parent_id=0)
    """
    # decorators = [jwt_required()]

    def __init__(self):
        super().__init__(StockProductCategory,
                         CategorySchema(many=True),
                         StockProductCategory.parent_id)

    def get(self, id=None):
        """
        GET method to return all subCategorys of the given Category
        (parent_id=<CATEGORY_ID:0>)
        or all available categories
        """
        current_app.logger.debug('GET categories %s' % (repr(id)))
        return super().get(id)

    def post(self, id=0):
        return abort(405)

    def put(self, id=0):
        return abort(405)

    def delete(self, id=0):
        return abort(405)


class StockCategory(BaseResource):
    """
    Api to process single Category by it's ID
    """
    # decorators = [jwt_required()]

    def __init__(self):
        super().__init__(StockProductCategory,
                         CategorySchema(),
                         StockProductCategory.id)

    def get(self, id=0):
        """
        GET method to return the single Product by ID
        """
        current_app.logger.debug('GET category %d' % (id))
        return super().get(id)

    def put(self, id):
        """
        PUT method to modify the single Product by ID
        """
        current_app.logger.debug('PUT category %d' % (id))
        return super().put(id)

    def post(self):
        """
        POST method to add new entity
        """
        current_app.logger.debug('POST category')
        return super().post()

    def delete(self, id=0):
        """
        DELETE method to delete Category
        """
        current_app.logger.debug('DELETE category %d' % (id))
        return super().delete(id)

# url, resource, endpoint, description
endpoints = (
    ('/stock/categories', StockCategories,
     'categories_default', '[GET] Get all product categories'),
    ('/stock/categories_by_category_id/<int:id>', StockCategories,
     'category_by_category_id', '[GET] Get categories by parent category id'),
    ('/stock/category/<int:id>', StockCategory,
     'category_by_id', '[GET, PUT, DELETE] Individual category by id'),
    ('/stock/category', StockCategory,
     'add_category', '[POST] add new category')
)
