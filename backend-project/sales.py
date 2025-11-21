

from models import Sale, Receipt, User, Cart, Product, CartItem
from flask import request, jsonify
from flask.views import MethodView
from data import import_data, export_data
from datetime import datetime, date
from users_authentication import tokens, require_auth, require_auth_admin
import uuid


class SalesAPI(MethodView):

    @require_auth_admin
    def get(self):

        sales_list = [Sale.from_json(s) for s in import_data('./sales.json')]
        id_filter = request.args.get('id')
        date_filter = request.args.get('date')
        total_filter = request.args.get('total')
        product_id_filter = request.args.get('product_id')

        if id_filter:
            try:
                id_filter = int(id_filter)
            except ValueError as ex:
                return jsonify(message='id must be an integer')

        if total_filter:
            try:
                total_filter = float(total_filter)
            except ValueError as ex:
                return jsonify(message='total must be an integer or a float')
        
        if date_filter:
            try:
                datetime.strptime(date_filter, "%Y-%m-%d")
            except ValueError as ex:
                return jsonify(message='the date must be in this format YEAR-MONTH-DAY')
            
        if product_id_filter:
            try:
                product_id_filter = int(product_id_filter)
            except ValueError as ex:
                return jsonify(message='product_id must be an integer')
            
        filtered = sales_list

        if id_filter:
            filtered = [s for s in filtered if s.id == id_filter]
        
        if date_filter:
            filtered = [s for s in filtered if s.date == date_filter]

        if total_filter:
            filtered = [s for s in filtered if s.total == date_filter]

        if product_id_filter:
            filtered = [s for s in filtered if any(p.id == product_id_filter for p in s.products)]

        return jsonify([s.to_json() for s in filtered]), 200

    
    @require_auth
    def post(self):

        sales_list = [Sale.from_json(s, types_map={'products': CartItem}) for s in import_data('./sales.json')]
        receipts_list = [Receipt.from_json(r, types_map={'products': CartItem}) for r in import_data('./receipts.json')]
        users_list = [User.from_json(u) for u in import_data('./users.json')]
        carts_list = [Cart.from_json(c, types_map={'products': CartItem}) for c in import_data('./carts.json')]
        products_list = [Product.from_json(p) for p in import_data('./products.json')]
        request_body = request.json
        code = int(str(uuid.uuid4().int)[:10])
        token = request.headers.get('Authorization').split()[1]

        if not 'payment_method' in request_body:
            return jsonify(message='payment_method is required')
        
        if request_body['payment_method'] != 'sinpe':
            return jsonify(message='sinpe is the only payment method available')
        
        current_user = next((u for u in users_list if u.username == tokens[token]), None)

        if not current_user:
            return jsonify(message='invalid token'), 400
        
        current_cart = next((c for c in carts_list if c.user_id == current_user.id), None)

        if not current_cart:
            return jsonify(message='cart not found'), 404
        
        if current_cart.products == []:
            return jsonify(message='cart is empty'), 400
        
        new_sale = Sale(Sale.next_id(sales_list), current_user.id, current_cart.products, Sale.calculate_total(current_cart.products, products_list), None, request_body['payment_method'])

        sales_list.append(new_sale)

        current_cart.empty_cart()

        new_receipt = Receipt(Receipt.next_id(receipts_list), code, new_sale.id, new_sale.products, new_sale.total, new_sale.payment_method)
        receipts_list.append(new_receipt)

        export_data([s.to_json() for s in sales_list], './sales.json')
        export_data([c.to_json() for c in carts_list], './carts.json')
        export_data([r.to_json() for r in receipts_list], './receipts.json')

        return jsonify(new_receipt.to_public_json(products_list))
        

    @require_auth_admin
    def delete(self):

        sales_list = [Sale.from_json(s) for s in import_data('./sales.json')]
        receipts_list = [Receipt.from_json(r, types_map={'product': CartItem}) for r in import_data('./receipts.json')]
        request_body = request.json

        if 'receipt_code' not in request_body:
            return jsonify(message='receipt_code is require'), 400
        
        if request_body['receipt_code']:
            try:
                request_body['receipt_code'] = int(request_body['receipt_code'])
            except ValueError:
                return jsonify(message='receipt code must be numbers')
            
        user_receipt = next((r for r in receipts_list if r.code == request_body['receipt_code']), None)

        if not user_receipt:
            return jsonify(message='receipt not found'), 404
            
        
        user_sale = next((s for s in sales_list if s.id == user_receipt.sale_id), None)

        if not user_sale:
            return jsonify(message='sale not found'), 404
        
        sales_list = [s for s in sales_list if s.id != user_sale.id]
        export_data([s.to_json() for s in sales_list], './sales.json')

        return jsonify(message=f'sale deleted'), 200
        


def register_api(app):
    sales_view = SalesAPI.as_view('sales_api')
    app.add_url_rule('/sales', view_func=sales_view, methods=['GET', 'POST', 'DELETE'])
