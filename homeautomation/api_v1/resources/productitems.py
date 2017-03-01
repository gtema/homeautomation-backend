from flask import jsonify, make_response, abort

from homeautomation.models import db, StockProductItem
from homeautomation.schemas import ProductItemSchema

from .base import BaseResource


class StockCategoryProductItems(BaseResource):
    '''
    Api to return all product items of the given product
    '''
    # decorators = [jwt_required()]

    def __init__(self):
        super().__init__(StockProductItem,
                         ProductItemSchema(many=True),
                         StockProductItem.product_id)

    def get(self, id):
        return super().get(id)

    def post(self, id=0):
        return abort(405)

    def put(self, id=0):
        return abort(405)

    def delete(self, id=0):
        return abort(405)


class StockCategoryProductItem(BaseResource):
    '''
    Api to provide access (add, delete, modify) to single product item
    '''
    # decorators = [jwt_required()]

    def __init__(self):
        super().__init__(StockProductItem,
                         ProductItemSchema(many=False),
                         StockProductItem.id)

    def get(self, id):
        return super().get(id)

    def put(self, id):
        '''
        PUT method to modify the single ProductItem by ID
        '''
        return super().put(id)

    def post(self):
        '''
        POST method to add a new product item
        '''
        return super().post()

    def delete(self, id=0):
        '''
        DELETE method to mark item as consumed
        no ID is expected. Entity, marked as started, will be "consumed"
        '''
        try:
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

            return make_response('', 204)
            
        except DatabaseError as e:
            res = make_response(
                        jsonify({'Internal Exception during product item deletion': str(e)}),
                        500)
