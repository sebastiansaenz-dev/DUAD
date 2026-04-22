

from flask import request, jsonify, Blueprint
from flask.views import MethodView
from models import Orders
from schemas.orders_schema import OrdersSchema
from repos.orders_repo import OrdersRepo
from utils import require_admin, require_auth, handle_errors


orders_bp = Blueprint('orders', __name__, url_prefix='/orders')

class OrdersAPI(MethodView):

    def __init__(self):
        self.repo = OrdersRepo(Orders, OrdersSchema())


    @require_auth
    @handle_errors
    def get(self, current_user_id):

        orders = self.repo.get_all({'user_id': current_user_id})
        return jsonify(orders)


    @require_auth
    @handle_errors
    def post(self, current_user_id):
        new_order = self.repo.create_order(current_user_id)

        return jsonify(new_order)

order_view = OrdersAPI.as_view('order_api')
orders_bp.add_url_rule('/', view_func=order_view, methods=['GET', 'POST'])

