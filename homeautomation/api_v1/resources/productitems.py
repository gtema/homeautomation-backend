from flask import jsonify, make_response, abort, current_app

from homeautomation.models import db, StockProductItem
from homeautomation.schemas import ProductItemSchema
from sqlalchemy.exc import DatabaseError

from .base import BaseResource


class StockCategoryProductItems(BaseResource):
    """
    Api to return all product items of the given product
    """
    # decorators = [jwt_required()]

    def __init__(self):
        super().__init__(StockProductItem,
                         ProductItemSchema(many=True),
                         StockProductItem.product_id)

    def get(self, id):
        current_app.logger.debug('GET productItems %s' % (repr(id)))
        return super().get(id)

    def post(self, id=0):
        return abort(405)

    def put(self, id=0):
        return abort(405)

    def delete(self, id=0):
        return abort(405)


class StockCategoryProductItem(BaseResource):
    """
    Api to provide access (add, delete, modify) to single product item
    """
    # decorators = [jwt_required()]

    def __init__(self):
        super().__init__(StockProductItem,
                         ProductItemSchema(many=False),
                         StockProductItem.id)

    def get(self, id):
        current_app.logger.debug('GET productItem %s' % (repr(id)))
        return super().get(id)

    def put(self, id):
        """
        PUT method to modify the single ProductItem by ID
        """
        current_app.logger.debug('PUT productItem %s' % (repr(id)))
        return super().put(id)

    def post(self):
        """
        POST method to add a new product item
        """
        current_app.logger.debug('POST productItem')
        return super().post()

    def delete(self, id=0):
        """
        DELETE method to mark item as consumed
        no ID is expected. Entity, marked as started, will be "consumed"
        """
        current_app.logger.debug('DELETE productItem %s' % (repr(id)))
        try:
            if id:
                item = self.model.query.filter(self.model.id == id).\
                            first_or_404()
            else:
                item = self.model.query.filter(StockProductItem.is_started).\
                            first()
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
            return make_response(
                        jsonify({'Internal Exception during product '
                                 'item deletion': str(e)}),
                        500)
