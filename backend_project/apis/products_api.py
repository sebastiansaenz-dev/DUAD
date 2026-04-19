

from flask.views import MethodView
from flask import request, jsonify
from repos.products_repo import ProductsRepo
from models import Products
from schemas.products_schema import ProductsSchema
from utils import handle_errors



class ProductsAPI(MethodView):
    def __init__(self):
        self.repo = ProductsRepo(Products, ProductsSchema())

    @handle_errors
    def get(self):
        filters = request.args

        products = self.repo.get_all(filters)

        return jsonify(products)


def register_api(app):
    products_view = ProductsAPI.as_view('products_api')
    app.add_url_rule('/products', view_func=products_view, methods=['GET'])
