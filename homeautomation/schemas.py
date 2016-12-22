from homeautomation import ma
from homeautomation.models import StockProductCategory,  StockProduct,  StockProductItem
from marshmallow import fields,  ValidationError

def must_not_be_blank(data):
    if not data:
        raise ValidationError('Data not provided')

class CategorySchema(ma.ModelSchema):
    '''
    Stock product group SER/DE
    '''
    class Meta:
        model = StockProductCategory
    
    id = fields.Int(dump_only = True)
    parent_id = fields.Int()
    name = fields.Str(required = True)

class ProductSchema(ma.ModelSchema):
    '''
    Stock product SER/DE
    '''
    class Meta:
        model = StockProduct
#        fields = ('id',  'category_id',  'name',  'volume',  'count_quantities',  'amount',  'first_started_id',  'first_started_ed')

    id = fields.Int(dump_only = True)
    category_id = fields.Int(required = True,  validate = must_not_be_blank)
    name = fields.Str(required = True)
    volume = fields.Str()
    count_quantities = fields.Boolean()
    amount = fields.Int(dump_only = True)
    first_started_id = fields.Int(dump_only = True)
    first_started_ed = fields.Date(dump_only = True)

class ProductItemSchema(ma.ModelSchema):
    '''
    Stock product item SER/DE
    '''
    class Meta:
        model = StockProductItem

    id = fields.Int(dump_only = True)
    product_id = fields.Int(required = True,  validate = must_not_be_blank)
    is_started = fields.Boolean()
    expiry_date = fields.Date()

