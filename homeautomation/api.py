"""
API for the HomeAutomation (CRUD services)
"""
from flask import Blueprint, request, jsonify, make_response, abort
from flask_restful import Api, Resource
from flask_login import login_required
from . import db
from .models import StockProductCategory, StockProduct,\
                                  StockProductItem
from .schemas import CategorySchema, ProductSchema, \
                                   ProductItemSchema


class BaseCrud(Resource):
    '''
    Base CRUD services class
    it requires SQLAlchemy model, Marshmallow schema and model qualifier
    (i.e. ID, PARENT_ID) to be set in the constructor
    '''

    def __init__(self,  model,  schema,  qualifier):
        '''
        Constructor, setting model, schema and filter qualifier
        '''
        self.schema = schema
        self.model = model
        self.qualifier = qualifier

    def get(self,  id):
        '''
        GET method to get JSON representation of items by qualifier
        '''
        if (id is not None):
            items = self.model.query.filter(self.qualifier == id)
        else:
            items = self.model.query.all()

        if self.schema.many:
            # multiple items
            res = self.schema.dump(items).data
        else:
            # single item
            res = self.schema.dump(items.first()).data

        return res

    def put(self, id=0):
        '''
        PUT method to modify existing item
        '''
        json = request.get_json()

        if not json:
            return make_response(jsonify({'message': 'No input'}), 400)

        if id == 0:
            return make_response(
                        jsonify({'message': 'ID is missing or wrong'}),
                        400)

        item = self.model.query.filter(self.qualifier == id).first_or_404()

        data, errors = self.schema.load(json,
                                        instance=item,
                                        session=db.session)

        if errors:
            return make_response(jsonify(errors),  422)

        db.session.commit()

        return self.schema.dump(item).data

    def post(self):
        '''
        POST method to add a new item
        '''
        json = request.get_json()

        if not json:
            return make_response(jsonify({'message': 'No input'}), 400)

        item,  errors = self.schema.load(json)
        if errors:
            return make_response(jsonify(errors),  422)
        db.session.add(item)
        db.session.commit()

        return make_response(self.schema.jsonify(item), 201)

    def delete(self,  id=0):
        '''
        DELETE method to drop product
        '''

        if id == 0:
            return make_response(jsonify({'message': 'Id not given'}), 422)

        item = self.model.query.filter(self.model.id == id).first_or_404()

#        if not item:
#            return make_response(jsonify({'message': 'Entity not found'}),422)

        db.session.delete(item)
        db.session.commit()

        return make_response(jsonify({'message': 'ok'}), 200)

'''
API classes
'''


class StockCategories(BaseCrud):
    '''
    Api to return all subCategorys of the given Category (or root, parent_id=0)
    '''
    decorators = [login_required]

    def __init__(self):
        super().__init__(StockProductCategory,
                         CategorySchema(many=True),
                         StockProductCategory.parent_id)

    def get(self,  id=None):
        '''
        GET method to return all subCategorys of the given Category
        (parent_id=<CATEGORY_ID:0>)
        '''
        return super().get(id)

    def post(self, id=0):
        return abort(405)

    def put(self, id=0):
        return abort(405)

    def delete(self, id=0):
        return abort(405)


class StockCategory(BaseCrud):
    '''
    Api to process single Category by it's ID
    '''
    decorators = [login_required]

    def __init__(self):
        super().__init__(StockProductCategory,
                         CategorySchema(),
                         StockProductCategory.id)

    def get(self,  id=0):
        '''
        GET method to return the single Product by ID
        '''
        return super().get(id)

    def put(self,  id):
        '''
        PUT method to modify the single Product by ID
        '''
        return super().put(id)

    def post(self):
        '''
        POST method to add new entity
        '''
        return super().post()

    def delete(self,  id=0):
        '''
        DELETE method to delete Category
        '''
        item = StockProductCategory.query.\
            filter(StockProductCategory.id == id).\
            first_or_404()

        if not item:
            return make_response(jsonify({'message': 'Category not found'}),
                                 422
                                 )

        db.session.delete(item)
        db.session.commit()
        return make_response(jsonify({'message': 'ok'}), 200)


class StockCategoryProducts(BaseCrud):
    '''
    Api to return all products belonging to the Category
    '''
    decorators = [login_required]

    def __init__(self):
        super().__init__(StockProduct,
                         ProductSchema(many=True),
                         StockProduct.category_id)

    def get(self,  id):
        return super().get(id)

    def post(self, id=0):
        return abort(405)

    def put(self, id=0):
        return abort(405)

    def delete(self, id=0):
        return abort(405)


class StockCategoryProduct(BaseCrud):
    '''
    Api for working with a single product
    '''
    decorators = [login_required]

    def __init__(self):
        super().__init__(StockProduct, ProductSchema(), StockProduct.id)

    def get(self,  id=-1):
        '''
        GET method to return the single Product by ID
        '''
        if id == -1:
            return make_response(
                    jsonify({
                     'message': 'Product GET without ID is not allowed'
                    }),
                    422)
        else:
            return super().get(id)

    def put(self,  id=-1):
        '''
        PUT method to modify the single Product by ID
        '''
        if id == -1:
            return make_response(
                            jsonify({
                             'message': 'Product PUT without ID is not allowed'
                            }),
                            422)
        else:
            return super().put(id)

    def post(self):
        '''
        POST method to add new entity
        '''
        return super().post()

    def delete(self,  id=-1):
        '''
        DELETE method to drop product
        '''
        if id == -1:
            return make_response(
                        jsonify({
                          'message': 'Product DELETE without ID is not allowed'
                        }),
                        422)
        item = StockProduct.query.filter(StockProduct.id == id).first_or_404()

        if not item:
            return make_response(
                        jsonify({
                            'message': 'Product not found'
                        }),
                        422)

        db.session.delete(item)
        db.session.commit()

        return make_response(jsonify({'message': 'ok'}), 200)


class StockCategoryProductItems(BaseCrud):
    '''
    Api to return all product items of the given product
    '''
    decorators = [login_required]

    def __init__(self):
        super().__init__(StockProductItem,
                         ProductItemSchema(many=True),
                         StockProductItem.product_id)

    def get(self,  id):
        return super().get(id)

    def post(self, id=0):
        return abort(405)

    def put(self, id=0):
        return abort(405)

    def delete(self, id=0):
        return abort(405)


class StockCategoryProductItem(BaseCrud):
    '''
    Api to provide access (add, delete, modify) to single product item
    '''
    decorators = [login_required]

    def __init__(self):
        super().__init__(StockProductItem,
                         ProductItemSchema(many=False),
                         StockProductItem.id)

    def get(self,  id):
        return super().get(id)

    def put(self,  id):
        '''
        PUT method to modify the single ProductItem by ID
        '''
        return super().put(id)

    def post(self):
        '''
        POST method to add a new product item
        '''
        return super().post()

    def delete(self,  id=0):
        '''
        DELETE method to mark item as consumed
        no ID is expected. Entity, marked as started, will be "consumed"
        '''
        if id:
            item = self.model.query.filter(self.model.id == id).first_or_404()
        else:
            item = self.model.query.filter(StockProductItem.is_started).first()
            if not item:
                return make_response(
                                jsonify({
                                 'message': 'No started entity found'
                                }),
                                422)

        if item:
            db.session.delete(item)
            db.session.commit()

        return make_response(jsonify({'message': 'ok'}), 200)


api_bp = Blueprint('api',  __name__)
api = Api(api_bp)

# Get subCategorys by category_id
api.add_resource(StockCategories,
                 '/stock/categories_by_category_id/<int:id>',
                 endpoint='categories_by_category_id')
api.add_resource(StockCategories,
                 '/stock/categories',
                 endpoint='categories_default')
# ADD, MODIFY, DELETE
api.add_resource(StockCategory,
                 '/stock/category/<int:id>',
                 endpoint='category_by_id')
api.add_resource(StockCategory,
                 '/stock/category',
                 endpoint='add_category')

# GET<Products_by_ID>
api.add_resource(StockCategoryProducts,
                 '/stock/products_by_category_id/<int:id>',
                 endpoint='products_by_category')

# GET<Product_by_ID>, Add, Modify, Delete
api.add_resource(StockCategoryProduct,
                 '/stock/product/<int:id>',
                 endpoint='product_by_id')
api.add_resource(StockCategoryProduct,
                 '/stock/product',
                 endpoint='add_product')

# Get<Items_by_productID>
api.add_resource(StockCategoryProductItems,
                 '/stock/product_items_by_product_id/<int:id>',
                 endpoint='product_items_by_product')

# Add new product Item, Delete (consume entity)
api.add_resource(StockCategoryProductItem,
                 '/stock/product_item/<int:id>',
                 endpoint='alter_product_item')
api.add_resource(StockCategoryProductItem,
                 '/stock/product_item',
                 endpoint='add_product_item')
