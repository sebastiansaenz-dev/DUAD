

from flask import request, jsonify, Blueprint
from flask.views import MethodView
from models import Orders
from schemas.orders_schema import OrdersSchema
from repos.admin_repos.admin_orders_repo import AdminOrdersRepo
from utils import require_admin, handle_errors


admin_orders_bp = Blueprint('admin_orders', __name__, url_prefix='/staff-portal/orders')

class AdminOrdersAPI(MethodView):

    def __init__(self):
        self.repo = AdminOrdersRepo(Orders, OrdersSchema())


    @require_admin
    @handle_errors
    def get(self):
        filters = request.args

        orders = self.repo.get_all(filters)
        return jsonify(orders)


    @require_admin
    @handle_errors
    def post(self, id):
        new_order = self.repo.create_order(id)

        return jsonify(new_order)

    @require_admin
    @handle_errors
    def patch(self, id):
        data = request.get_json()

        order = self.repo.update_status(id, data)

        return jsonify(order)

admin_order_view = AdminOrdersAPI.as_view('admin_order_api')
admin_orders_bp.add_url_rule('/', view_func=admin_order_view, methods=['GET'])
admin_orders_bp.add_url_rule('/<int:id>', view_func=admin_order_view, methods=['POST', 'PATCH'])



