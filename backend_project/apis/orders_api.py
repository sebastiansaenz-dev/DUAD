

from flask import jsonify, Blueprint
from flask.views import MethodView
from utils import require_auth, handle_errors
from services.order_service import OrderService


orders_bp = Blueprint('orders', __name__, url_prefix='/orders')

class OrdersAPI(MethodView):

    def __init__(self):
        self.service = OrderService()


    @require_auth
    @handle_errors
    def get(self, current_user_id):

        orders = self.service.repo.get_all({'user_id': current_user_id})
        return jsonify(orders)


    @require_auth
    @handle_errors
    def post(self, current_user_id):
        new_order = self.service.create_order(current_user_id)

        return jsonify(self.service.repo.schema.dump(new_order))

order_view = OrdersAPI.as_view('order_api')
orders_bp.add_url_rule('/', view_func=order_view, methods=['GET', 'POST'])

