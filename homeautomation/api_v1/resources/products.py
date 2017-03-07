from flask import jsonify, make_response, abort, current_app

from homeautomation.models import StockProduct
from homeautomation.schemas import ProductSchema

from .base import BaseResource


class StockCategoryProducts(BaseResource):
    """
    Api to return all subCategorys of the given Category (or root, parent_id=0)
    """
    # decorators = [jwt_required()]

    def __init__(self):
        super().__init__(StockProduct,
                         ProductSchema(many=True),
                         StockProduct.category_id)

    def get(self, id):
        current_app.logger.debug('GET products %s' % (repr(id)))
        return super().get(id)

    def post(self, id=0):
        return abort(405)

    def put(self, id=0):
        return abort(405)

    def delete(self, id=0):
        return abort(405)


class StockCategoryProduct(BaseResource):
    """
    Api to process single Category by it's ID
    """
    # decorators = [jwt_required()]

    def __init__(self):
        super().__init__(StockProduct, ProductSchema(), StockProduct.id)

    def get(self, id=0):
        """
        GET method to return the single Product by ID
        """
        current_app.logger.debug('GET product %s' % (repr(id)))
        if id == 0:
            return make_response(
                jsonify({
                    'message': 'Product GET without ID is not allowed'
                }),
                422)
        else:
            return super().get(id)

    def put(self, id=0):
        """
        PUT method to modify the single Product by ID
        """
        current_app.logger.debug('PUT product %s' % (repr(id)))
        return super().put(id)

    def post(self):
        """
        POST method to add new entity
        """
        current_app.logger.debug('POST product')
        return super().post()

    def delete(self, id=0):
        """
        DELETE method to drop product
        """
        current_app.logger.debug('DELETE product %s' % (repr(id)))
        return super().delete(id)

# url, resource, endpoint, description
endpoints = (
    ('/stock/products_by_category_id/<int:id>', StockCategoryProducts,
     'products_by_category', '[GET] all products of a given category'),
    ('/stock/product/<int:id>', StockCategoryProduct,
     'product_by_id', '[GET, PUT, DELETE] individual product'),
    ('/stock/product', StockCategoryProduct,
     'add_product', '[POST] add a new product')
)
