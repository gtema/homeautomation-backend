from flask_cors import CORS
from flask_restful import Api
from flask import Blueprint, abort, jsonify
from homeautomation.api_v1.resources.categories import StockCategories, StockCategory
from homeautomation.api_v1.resources.products import StockCategoryProducts, StockCategoryProduct
from homeautomation.api_v1.resources.productitems import StockCategoryProductItems, StockCategoryProductItem


api_bp = Blueprint('api', __name__)
api = Api(api_bp)

api.init_app(api_bp)
CORS(api_bp)

@api_bp.route('/')
def show():
    return 'Hello World API'

# All categories
api.add_resource(StockCategories,
                 '/stock/categories',
                 endpoint='categories_default')
# Get subCategorys by category_id
api.add_resource(StockCategories,
                 '/stock/categories_by_category_id/<int:id>',
                 endpoint='categories_by_category_id')
# ADD, MODIFY, DELETE
api.add_resource(StockCategory,
                 '/stock/category/<int:id>',
                 endpoint='category_by_id')
# ADD category
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
# Add product
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
