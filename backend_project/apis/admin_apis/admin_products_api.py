

from flask.views import MethodView
from flask import request, jsonify, Blueprint
from utils import handle_errors, require_auth
from services.admin_services.admin_product_service import AdminProductService


admin_products_bp = Blueprint('admin_products', __name__, url_prefix='/staff-portal/products')


class AdminProductsAPI(MethodView):
    def __init__(self):
        self.service = AdminProductService()

    @require_auth(role='admin')
    @handle_errors
    def post(self):
        data = request.get_json()

        new_item = self.service.create_product(data)

        return jsonify(new_item)
    

    @require_auth(role='admin')
    @handle_errors
    def patch(self, id):
        data = request.get_json()

        updated_item = self.service.update_product(id, data)

        return jsonify(updated_item)


    @require_auth(role='admin')
    @handle_errors
    def delete(self, id):
        deleted_item = self.service.delete_product(id)

        if deleted_item:
            return jsonify(message='item deleted'), 200


admin_products_view = AdminProductsAPI.as_view('admin_products_api')
admin_products_bp.add_url_rule('/', view_func=admin_products_view, methods=['POST'])
admin_products_bp.add_url_rule('/<int:id>', view_func=admin_products_view, methods=['PATCH', 'DELETE'])
