from flask import jsonify, make_response, abort, current_app
from flask_restful import reqparse

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
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, help='Product name')
        self._parser = parser

    def get(self, id=0):
        current_app.logger.debug('GET products %s' % (repr(id)))
        args = self._parser.parse_args()
        if 'name' in args and args['name'] is not None:
            print("Requesting products with name %s" % args['name'])
            return super().get_by_name(args['name'])
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
    ('/stock/products', StockCategoryProducts,
     'products_with_filter', '[GET] all products with a name filter '
     '(given as request parameter)'),
    ('/stock/products_by_category_id/<int:id>', StockCategoryProducts,
     'products_by_category', '[GET] all products of a given category'),
    ('/stock/product/<int:id>', StockCategoryProduct,
     'product_by_id', '[GET, PUT, DELETE] individual product'),
    ('/stock/product', StockCategoryProduct,
     'add_product', '[POST] add a new product')
)
