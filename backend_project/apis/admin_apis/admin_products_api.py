

from flask.views import MethodView
from flask import request, jsonify
from repos.products_repo import ProductsRepo
from models import Products
from schemas.products_schema import ProductsSchema
from utils import handle_errors, require_admin
import uuid



class AdminProductsAPI(MethodView):
    def __init__(self):
        self.repo = ProductsRepo(Products, ProductsSchema())

    @require_admin
    @handle_errors
    def post(self):
        data = request.get_json()

        sku = uuid.uuid4().hex.upper()[:10]

        data['sku'] = sku

        new_item = self.repo.create(data)

        return jsonify(new_item)
    

    @require_admin
    @handle_errors
    def patch(self, id):
        data = request.get_json()

        updated_item = self.repo.update(id, data)

        return jsonify(updated_item)


    @require_admin
    @handle_errors
    def delete(self, id):
        deleted_item = self.repo.delete(id)

        if deleted_item:
            return jsonify(message='item deleted'), 200


def register_api(app):
    admin_products_view = AdminProductsAPI.as_view('admin_products_api')
    app.add_url_rule('/staff-portal/products', view_func=admin_products_view, methods=['POST'])
    app.add_url_rule('/staff-portal/products/<int:id>', view_func=admin_products_view, methods=['PATCH', 'DELETE'])