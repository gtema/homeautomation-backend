from marshmallow import fields, ValidationError
from flask_marshmallow import Marshmallow

from .models import User, Role, StockProductCategory, StockProduct,\
    StockProductItem

ma = Marshmallow()


def must_not_be_blank(data):
    if not data:
        raise ValidationError('Data not provided')


class UserSchema(ma.ModelSchema):
    '''
    User schema
    '''
    class Meta:
        model = User

    id = fields.Int(dump_only=True)
    username = fields.Str()


class RoleSchema(ma.ModelSchema):
    '''
    Role schema
    '''
    class Meta:
        model = Role

    # Validates for the different fields
    id = fields.Integer(dump_only=True)
    name = fields.String(validate=must_not_be_blank)
    description = fields.String(validate=must_not_be_blank)


class CategorySchema(ma.ModelSchema):
    '''
    Stock category SER/DE
    '''
    class Meta:
        model = StockProductCategory

    id = fields.Int(dump_only=True)
    parent_id = fields.Int()
    name = fields.Str(required=True)
    prio = fields.Int()


class ProductSchema(ma.ModelSchema):
    '''
    Stock product SER/DE
    '''
    class Meta:
        model = StockProduct

    id = fields.Int(dump_only=True)
    category_id = fields.Int(required=True, validate=must_not_be_blank)
    name = fields.Str(required=True)
    volume = fields.Str()
    sum_amounts = fields.Boolean()
    amount = fields.Int(dump_only=True)
    first_started_id = fields.Int(dump_only=True)
    first_started_ed = fields.Date(dump_only=True)


class ProductItemSchema(ma.ModelSchema):
    '''
    Stock product item SER/DE
    '''
    class Meta:
        model = StockProductItem

    id = fields.Int(dump_only=True)
    product_id = fields.Int(required=True, validate=must_not_be_blank)
    is_started = fields.Boolean()
    is_disposed = fields.Boolean()
    expiry_date = fields.Date()
    is_valid = fields.Boolean(dump_only=True)
