from flask import Blueprint, jsonify, make_response
from flask_restful import Api

from homeautomation.api_v1.resources.categories import \
    endpoints as categoriesEps
from homeautomation.api_v1.resources.products import\
    endpoints as productEps
from homeautomation.api_v1.resources.productitems import\
    endpoints as productItemEps


api_bp = Blueprint('api', __name__)
api = Api(api_bp)

api.init_app(api_bp)

# url, resource, endpoint, description
endpoints = categoriesEps + productEps + productItemEps


@api_bp.route('/')
def index():
    """Api root request - lists supported endpoints
    """
    api_descriptions = {url: description
                        for (url, resource, endpoint, description) in endpoints
                        }
    api_descriptions['api'] = 'Homeautomation API'
    return make_response(jsonify(api_descriptions), 200)


def register():
    """ Register resources
    """
    for (url, resource, _endpoint, description) in endpoints:
        api.add_resource(resource, url, endpoint=_endpoint)

# Register supported resources
register()
