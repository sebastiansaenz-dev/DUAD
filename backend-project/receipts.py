


from flask.views import MethodView
from flask import request, jsonify
from data import import_data, receipts_path
from models import Receipt, CartItem
from users_authentication import require_auth_admin
from utils import validate_int, validate_date, handle_errors


class ReceiptAPI(MethodView):
    @require_auth_admin
    @handle_errors
    def get(self):

        receipts_list = [Receipt.from_json(r, types_map={'products': CartItem}) for r in import_data(receipts_path)]
        id_filter = request.args.get('id')
        code_filter = request.args.get('code')
        sale_id_filter = request.args.get('sale_id')
        product_id_filter = request.args.get('product_id')
        total_filter = request.args.get('total')
        date_filter = request.args.get('date')

        if date_filter:
            date_filter = validate_date(date_filter)

        if id_filter:
            id_filter = validate_int(id_filter, 'id')

        if user_id_filter:
            user_id_filter = validate_int(user_id_filter, 'user_id')

        if product_id_filter:
            product_id_filter = validate_int(product_id_filter, 'product_id')

        if total_filter:
            total_filter = validate_int(total_filter, 'total')
            
            
        filtered = receipts_list

        if id_filter:
            filtered = [r for r in receipts_list if r.id == id_filter]

        if code_filter:
            filtered = [r for r in receipts_list if r.code == code_filter]

        if sale_id_filter:
            filtered = [r for r in receipts_list if r.sale_id == sale_id_filter]

        if product_id_filter:
            filtered = [r for r in receipts_list if any(p.product_id == product_id_filter for p in r.products)]

        if total_filter:
            filtered = [r for r in receipts_list if r.total == total_filter]

        if date_filter:
            filtered = [r for r in receipts_list if r.date == date_filter]

        return jsonify([r.to_json() for r in filtered]), 200


def register_api(app):
    receipt_view = ReceiptAPI.as_view('receipt_api')
    app.add_url_rule('/receipts', view_func=receipt_view, methods=['GET'])
