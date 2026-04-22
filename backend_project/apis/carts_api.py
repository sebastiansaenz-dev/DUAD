


from flask import request, jsonify, Blueprint
from flask.views import MethodView
from models import Carts
from schemas.carts_schema import CartsSchema
from repos.carts_repo import CartsRepo
from utils import require_auth, handle_errors
from constants import CartsStatusEnum


carts_bp = Blueprint('carts', __name__, url_prefix='/cart')

class CartsAPI(MethodView):
    def __init__(self):
        self.repo = CartsRepo(Carts, CartsSchema())

    @require_auth
    @handle_errors
    def get(self, current_user_id):

        cart = self.repo.get_one({'user_id': current_user_id, "status_id": CartsStatusEnum.ACTIVE})

        if not cart:
            return jsonify('nothing in your cart')


        products = [{
            'name': p.product.name,
            'price': p.product.price,
            'quantity': p.quantity,
            'total': p.product.price * p.quantity
        } for p in cart.items]


        total = 0

        for p in products:
            total += p['total']


        return jsonify({
            'cart_products': products,
            'total': total
        })
    
    
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



