


from flask import request, jsonify, Blueprint
from flask.views import MethodView
from models import Carts
from schemas.carts_schema import CartsSchema
from repos.carts_repo import CartsRepo
from utils import require_auth, handle_errors


carts_bp = Blueprint('carts', __name__, url_prefix='/cart')

class CartsAPI(MethodView):
    def __init__(self):
        self.repo = CartsRepo(Carts, CartsSchema())

    @require_auth
    @handle_errors
    def get(self, current_user_id):

        return jsonify(self.repo.get_cart(current_user_id))
    

    @require_auth
    @handle_errors
    def post(self, current_user_id):
        data = request.get_json()

        self.repo.add_products(current_user_id, data)

        return jsonify('products added'), 201


    @require_auth
    @handle_errors
    def patch(self, current_user_id):
        data = request.get_json()

        self.repo.update_quantity(current_user_id, data)

        return jsonify(message='product updated')


    @require_auth
    @handle_errors
    def delete(self, current_user_id):
        data = request.get_json()

        self.repo.delete_product(current_user_id, data)

        return jsonify(message='product/s deleted')


carts_view = CartsAPI.as_view('carts_api')
carts_bp.add_url_rule('/', view_func=carts_view, methods=['GET', 'POST', 'PATCH', 'DELETE'])



