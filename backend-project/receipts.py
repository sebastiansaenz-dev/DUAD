


from flask.views import MethodView
from flask import request, jsonify
from data import import_data
from datetime import datetime
from models import Receipt
from users_authentication import require_auth_admin





class ReceiptAPI(MethodView):
    @require_auth_admin
    def get(self):

        receipts_list = [Receipt.from_json(r) for r in import_data('./receipts.json')]
        id_filter = request.args.get('id')
        code_filter = request.args.get('code')
        user_id_filter = request.args.get('user_id')
        sale_id_filter = request.args.get('sale_id')
        product_id_filter = request.args.get('product_id')
        total_filter = request.args.get('total')
        date_filter = request.args.get('date')

        if date_filter:
            try:
                datetime.strptime(date_filter, '%Y-%m-%d')
            except ValueError as ex:
                return jsonify(message='date must be in format YYYY-MM-DD')
            
        if id_filter:
            try:
                id_filter = int(id_filter)
            except ValueError as ex:
                return jsonify(message='the id must be an integer'), 400

        if user_id_filter:
            try:
                user_id_filter = int(user_id_filter)
            except ValueError as ex:
                return jsonify(message='the user_id must be an integer'), 400
            
        if product_id_filter:
            try:
                product_id_filter = int(product_id_filter)
            except ValueError as ex:
                return jsonify(message='the product_id must be an integer'), 400
            
        if total_filter:
            try:
                total_filter = int(total_filter)
            except ValueError as ex:
                return jsonify(message='the total must be an integer'), 400
            
        filtered = receipts_list

        if id_filter:
            filtered = [r for r in receipts_list if r.id == id_filter]

        if code_filter:
            filtered = [r for r in receipts_list if r.code == code_filter]
        
        if user_id_filter:
            filtered = [r for r in receipts_list if r.user_id == user_id_filter]

        if sale_id_filter:
            filtered = [r for r in receipts_list if r.sale_id == sale_id_filter]

        if product_id_filter:
            filtered = [r for r in receipts_list if r.product_id == product_id_filter]

        if total_filter:
            filtered = [r for r in receipts_list if r.total == total_filter]

        if date_filter:
            filtered = [r for r in receipts_list if r.date == date_filter]

        return jsonify([r.to_json() for r in filtered]), 200


def register_api(app):
    receipt_view = ReceiptAPI.as_view('receipt_api')
    app.add_url_rule('/receipts', view_func=receipt_view, methods=['GET'])
