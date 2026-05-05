

from flask.views import MethodView
from flask import request, jsonify, Blueprint
from utils import handle_errors
from services.product_service import ProductService

products_bp = Blueprint('products', __name__, url_prefix='/products')



class ProductsAPI(MethodView):
    def __init__(self):
        self.service = ProductService()


    @handle_errors
    def get(self, id=None):

        if id:
            return jsonify(self.service.get(page=1, per_page=1, id=id))

        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        filters = request.args.to_dict()

        return jsonify(self.service.get(page, per_page, filters=filters))



products_view = ProductsAPI.as_view('products_api')

products_bp.add_url_rule('/', view_func=products_view, methods=['GET'])
products_bp.add_url_rule('/<int:id>', view_func=products_view, methods=['GET'])

