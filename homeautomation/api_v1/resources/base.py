from flask import request, jsonify, make_response
from flask_restful import Resource
from sqlalchemy.exc import DatabaseError

from homeautomation.mysecurity import auth_required


class BaseResource(Resource):
    """
    Base CRUD services class
    it requires SQLAlchemy model, Marshmallow schema and model qualifier
    (i.e. ID, PARENT_ID) to be set in the constructor
    """
    decorators = [auth_required()]

    def __init__(self, model, schema, qualifier):
        """
        Constructor, setting model, schema and filter qualifier
        """
        self.schema = schema
        self.model = model
        self.qualifier = qualifier

    def get(self, id=0):
        """
        GET method to get JSON representation of items by qualifier

        :param id: entity__id__ attribute (__id__ is a self.qualifier)
        """
        # if id == -1:
        #     return make_response(
        #             jsonify({
        #              'message': 'Product GET without ID is not allowed'
        #             }),
        #             422)
        try:

            if (id is not None):
                items = self.model.query.filter(self.qualifier == id)
            else:
                items = self.model.query.filter(self.qualifier.isnot(None)).\
                    all()

            if self.schema.many:
                # multiple items
                res = make_response(self.schema.jsonify(items), 200)
            else:
                # single item
                # if nothing found return 404 (access by ID not found)
                res = make_response(self.schema.jsonify(items.first_or_404()),
                                    200)
        except DatabaseError as e:
            res = make_response(
                jsonify({'Internal Exception': str(e)}),
                500)

        return res

    def get_by_name(self, name):
        """
        GET items by name

        :param name: entity name

        """
        try:
            if (name is not None):
                items = self.model.query.filter(
                    self.model.name.ilike('%{}%'.format(name))
                )

            if self.schema.many:
                # multiple items
                res = make_response(self.schema.jsonify(items), 200)
            else:
                # single item
                # if nothing found return 404 (access by ID not found)
                res = make_response(self.schema.jsonify(items.first_or_404()),
                                    200)
        except DatabaseError as e:
            res = make_response(
                jsonify({'Internal Exception': str(e)}),
                500)

        return res

    def put(self, id=0):
        """
        PUT method to modify existing item

        :param id: entity__id__ attribute (__id__ is a self.qualifier)
        """
        json = request.get_json()

        if not json:
            return make_response(jsonify({'message': 'No input'}), 400)

        if id == 0:
            return make_response(
                jsonify({'message': 'ID is missing or wrong'}),
                400)

        try:
            # Find the item first
            item = self.model.query.filter(self.qualifier == id).first_or_404()

            # invoke base update method, passing schema and json.
            # They are used to load entity (schema.load)
            data, errors = item.update(self.schema, json)

            if errors:
                return make_response(jsonify(errors), 422)
            else:
                return make_response(self.schema.jsonify(item), 200)
        except DatabaseError as e:
            return make_response(
                jsonify({'Internal Exception during updating entity':
                        str(e)}
                        ),
                500)

    def post(self):
        """
        POST method to add a new item
        """
        json = request.get_json()

        if not json:
            return make_response(jsonify({'message': 'No input'}), 400)

        item, errors = self.schema.load(json)
        if errors:
            return make_response(jsonify(errors), 422)

        try:
            item.add(item)

            return make_response(self.schema.jsonify(item), 201)
        except DatabaseError as e:
            return make_response(
                jsonify({
                    'Internal Exception during creating new entity': str(e)
                }),
                500)

    def delete(self, id=0):
        """
        DELETE method to drop product
        delete without id will return 405

        :param id: entity__id__ attribute (__id__ is a self.qualifier)
        """
        if id == 0:
            return make_response(jsonify({
                'message': 'Entity DELETE without ID is not allowed'
            }), 405)
        # if id == 0:
        #     return make_response(jsonify({'message': 'Id not given'}), 422)

        try:
            item = self.model.query.filter(self.model.id == id).first_or_404()

            item.delete(item)
            return make_response('', 204)
        except DatabaseError as e:
            return make_response(
                jsonify({
                    'Internal Exception during creating new entity': str(e)
                }),
                500)
