from flask import jsonify, Blueprint, request
from flask.views import MethodView
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from utils import require_auth, handle_errors
from services.order_service import OrderService
from apis.resend_email_api import send_order_confirmation_email


orders_bp = Blueprint("orders", __name__, url_prefix="/orders")


class OrdersAPI(MethodView):
    def __init__(self):
        self.service = OrderService()

    @require_auth()
    @handle_errors
    def get(self, current_user_id):
        orders = self.service.repo.get_all({"user_id": current_user_id})
        return jsonify(orders)

    @handle_errors
    def post(self):
        data = request.get_json() or {}
        user_id = None

        verify_jwt_in_request(optional=True)
        identity = get_jwt_identity()
        if identity:
            user_id = identity

        new_order = self.service.create_order(user_id, data)
        send_order_confirmation_email(data.get("email"), new_order)

        return jsonify(self.service.repo.schema.dump(new_order))


order_view = OrdersAPI.as_view("order_api")
orders_bp.add_url_rule("/", view_func=order_view, methods=["GET", "POST"])
