

from flask import request, jsonify
from flask.views import MethodView
from models import Orders
from schemas.orders_schema import OrdersSchema
from repos.admin_repos.admin_orders_repo import AdminOrdersRepo
from utils import require_admin, handle_errors



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





def register_api(app):
    admin_order_view = AdminOrdersAPI.as_view('admin_order_api')
    app.add_url_rule('/staff-portal/orders', view_func=admin_order_view, methods=['GET'])
    app.add_url_rule('/staff-portal/orders/<int:id>', view_func=admin_order_view, methods=['POST', 'PATCH'])
