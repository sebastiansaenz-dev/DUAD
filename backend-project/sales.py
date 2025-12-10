

from models import Sale, Receipt, User, Cart, Product, CartItem
from flask import request, jsonify
from flask.views import MethodView
from data import import_data, export_data, sales_path, receipts_path, users_path, carts_path, products_path
from users_authentication import tokens, require_auth, require_auth_admin
import uuid
from utils import error_response, validate_int, validate_date, handle_errors


class SalesAPI(MethodView):

    @require_auth_admin
    @handle_errors
    def get(self):

        sales_list = [Sale.from_json(s) for s in import_data(sales_path)]
        id_filter = request.args.get('id')
        date_filter = request.args.get('date')
        total_filter = request.args.get('total')
        product_id_filter = request.args.get('product_id')

        if id_filter:
            id_filter = validate_int(id_filter, 'id')
        
        if total_filter:
            total_filter = validate_int(total_filter, 'total')

        if date_filter:
            date_filter = validate_date(date_filter)

        if product_id_filter:
            product_id_filter = validate_int(product_id_filter, 'product_id')
            
        filtered = sales_list

        if id_filter:
            filtered = [s for s in filtered if s.id == id_filter]
        
        if date_filter:
            filtered = [s for s in filtered if s.date == date_filter]

        if total_filter:
            filtered = [s for s in filtered if s.total == total_filter]

        if product_id_filter:
            filtered = [s for s in filtered if any(p.id == product_id_filter for p in s.products)]

        return jsonify([s.to_json() for s in filtered]), 200

    @require_auth
    @handle_errors
    def post(self):

        sales_list = [Sale.from_json(s, types_map={'products': CartItem}) for s in import_data(sales_path)]
        receipts_list = [Receipt.from_json(r, types_map={'products': CartItem}) for r in import_data(receipts_path)]
        users_list = [User.from_json(u) for u in import_data(users_path)]
        carts_list = [Cart.from_json(c, types_map={'products': CartItem}) for c in import_data(carts_path)]
        products_list = [Product.from_json(p) for p in import_data(products_path)]
        request_body = request.json
        code = int(str(uuid.uuid4().int)[:10])
        token = request.headers.get('Authorization').split()[1]

        if not 'payment_method' in request_body:
            return error_response('missing field: payment_method', 400)
        
        if request_body['payment_method'] != 'sinpe':
            return error_response('invalid payment method, allowed: sinpe', 400)
        
        current_user = next((u for u in users_list if u.username == tokens[token]), None)

        if not current_user:
            return error_response('invalid token', 401)
        
        current_cart = next((c for c in carts_list if c.user_id == current_user.id), None)

        if not current_cart:
            return error_response('cart not found', 404)
        
        if current_cart.products == []:
            return error_response('cart is empty', 400)
        
        new_sale = Sale(Sale.next_id(sales_list), current_user.id, current_cart.products, Sale.calculate_total(current_cart.products, products_list), None, request_body['payment_method'])

        sales_list.append(new_sale)

        current_cart.empty_cart()

        new_receipt = Receipt(Receipt.next_id(receipts_list), code, new_sale.id, new_sale.products, new_sale.total, new_sale.payment_method)
        receipts_list.append(new_receipt)

        export_data([s.to_json() for s in sales_list], sales_path)
        export_data([c.to_json() for c in carts_list], carts_path)
        export_data([r.to_json() for r in receipts_list], receipts_path)

        return jsonify(new_receipt.to_public_json(products_list)), 201
        

    @require_auth_admin
    @handle_errors
    def delete(self):

        sales_list = [Sale.from_json(s) for s in import_data(sales_path)]
        receipts_list = [Receipt.from_json(r, types_map={'product': CartItem}) for r in import_data(receipts_path)]
        request_body = request.json

        if 'receipt_code' not in request_body:
            return error_response('missing field: receipt_code', 400)
        
        if request_body['receipt_code']:
            try:
                request_body['receipt_code'] = int(request_body['receipt_code'])
            except ValueError:
                raise ValueError('receipt_code must be an integer')
            
        user_receipt = next((r for r in receipts_list if r.code == request_body['receipt_code']), None)

        if not user_receipt:
            return error_response('receipt not found', 404)
            
        user_sale = next((s for s in sales_list if s.id == user_receipt.sale_id), None)

        if not user_sale:
            return error_response('sale not found', 404)
        
        sales_list = [s for s in sales_list if s.id != user_sale.id]
        export_data([s.to_json() for s in sales_list], sales_path)

        return jsonify(message=f'sale deleted'), 200
        


def register_api(app):
    sales_view = SalesAPI.as_view('sales_api')
    app.add_url_rule('/sales', view_func=sales_view, methods=['GET', 'POST', 'DELETE'])
