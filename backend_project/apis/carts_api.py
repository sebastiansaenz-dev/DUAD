


from flask import request, jsonify, Blueprint
from flask.views import MethodView
from services.cart_service import CartService
from utils import require_auth, handle_errors


carts_bp = Blueprint('carts', __name__, url_prefix='/cart')

class CartsAPI(MethodView):
    def __init__(self):
        self.service = CartService()

    @require_auth()
    @handle_errors
    def get(self, current_user_id):

        return jsonify(self.service.get_cart(current_user_id))
    

    @require_auth()
    @handle_errors
    def post(self, current_user_id):
        data = request.get_json()

        self.service.add_products(current_user_id, data)

        return jsonify('products added'), 201


    @require_auth()
    @handle_errors
    def patch(self, current_user_id):
        data = request.get_json()

        self.service.update_quantity(current_user_id, data)

        return jsonify(message='product updated')


    @require_auth()
    @handle_errors
    def delete(self, current_user_id):
        data = request.get_json()

        self.service.delete_product(current_user_id, data)

        return jsonify(message='product/s deleted')


carts_view = CartsAPI.as_view('carts_api')
carts_bp.add_url_rule('/', view_func=carts_view, methods=['GET', 'POST', 'PATCH', 'DELETE'])



