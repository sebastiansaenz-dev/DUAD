from flask.views import MethodView
from flask import request, jsonify, Blueprint
from utils import handle_errors, require_auth
from services.category_service import CategoryService


categories_bp = Blueprint('categories', __name__, url_prefix='/categories')


class CategoriesAPI(MethodView):
    def __init__(self):
        self.service = CategoryService()

    @require_auth()
    @handle_errors
    def get(self, id=None):
        if id:
            return jsonify(self.service.get_by_id(id))

        filters = request.args.to_dict()
        return jsonify(self.service.get_all(filters))


categories_view = CategoriesAPI.as_view('categories_api')
categories_bp.add_url_rule('/', view_func=categories_view, methods=['GET'])
categories_bp.add_url_rule('/<int:id>', view_func=categories_view, methods=['GET'])
