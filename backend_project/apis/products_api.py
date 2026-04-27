

from flask.views import MethodView
from flask import request, jsonify, Blueprint
from repos.products_repo import ProductsRepo
from models import Products
from schemas.products_schema import ProductsSchema
from utils import handle_errors

products_bp = Blueprint('products', __name__, url_prefix='/products')



class ProductsAPI(MethodView):
    def __init__(self):
        self.repo = ProductsRepo(Products, ProductsSchema())

    @handle_errors
    def get(self):
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        filters = request.args.to_dict()

        products = self.repo.get_products(filters, page, per_page)

        return jsonify(products)


products_view = ProductsAPI.as_view('products_api')

products_bp.add_url_rule('/', view_func=products_view, methods=['GET'])

