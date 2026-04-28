


from flask import request, jsonify, Blueprint
from flask.views import MethodView
from models import Carts
from schemas.carts_schema import CartsSchema
from repos.admin_repos.admin_carts_repo import AdminCartsRepo
from utils import require_admin, handle_errors



admin_carts_bp = Blueprint('admin_carts', __name__, url_prefix='/staff-portal/carts')


class AdminCartsAPI(MethodView):
    def __init__(self):
        self.repo = AdminCartsRepo(Carts, CartsSchema())

    @require_admin
    @handle_errors
    def get(self):

        filters = request.args

        carts = self.repo.get_all(filters)

        return jsonify(carts)


    @require_admin
    @handle_errors
    def post(self, id):
        data = request.get_json()

        self.repo.add_products(id, data)

        return jsonify('products added'), 201


    @require_admin
    @handle_errors
    def patch(self, id):
        data = request.get_json()

        self.repo.update_quantity(id, data)

        return jsonify(message='product updated')


    @require_admin
    @handle_errors
    def delete(self, id):
        data = request.get_json()

        self.repo.delete_product(id, data)

        return jsonify(message='product/s deleted')
    

admin_carts_view = AdminCartsAPI.as_view('admin_carts_api')

admin_carts_bp.add_url_rule('/', view_func=admin_carts_view, methods=['GET'])
admin_carts_bp.add_url_rule('/<int:id>', view_func=admin_carts_view, methods=['POST', 'PATCH', 'DELETE'])






