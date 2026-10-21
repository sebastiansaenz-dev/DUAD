from flask.views import MethodView
from flask import request, jsonify, Blueprint
from utils import handle_errors, require_auth
from services.admin_services.admin_category_service import AdminCategoryService


admin_categories_bp = Blueprint('admin_categories', __name__, url_prefix='/staff-portal/categories')


class AdminCategoriesAPI(MethodView):
    def __init__(self):
        self.service = AdminCategoryService()

    @require_auth(role='admin')
    @handle_errors
    def get(self, id=None):
        if id:
            return jsonify(self.service.get_by_id(id))

        filters = request.args.to_dict()
        return jsonify(self.service.get_all(filters))

    @require_auth(role='admin')
    @handle_errors
    def post(self):
        data = request.get_json()
        new_item = self.service.create_category(data)
        return jsonify(new_item), 201

    @require_auth(role='admin')
    @handle_errors
    def patch(self, id):
        data = request.get_json()
        updated_item = self.service.update_category(id, data)
        return jsonify(updated_item)

    @require_auth(role='admin')
    @handle_errors
    def delete(self, id):
        deleted_item = self.service.delete_category(id)
        if deleted_item:
            return jsonify(message='item deleted'), 200


admin_categories_view = AdminCategoriesAPI.as_view('admin_categories_api')
admin_categories_bp.add_url_rule('/', view_func=admin_categories_view, methods=['GET', 'POST'])
admin_categories_bp.add_url_rule('/<int:id>', view_func=admin_categories_view, methods=['GET', 'PATCH', 'DELETE'])
