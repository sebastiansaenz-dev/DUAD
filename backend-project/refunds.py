

from flask.views import MethodView
from flask import request, jsonify
from data import import_data, export_data
from datetime import datetime, date
from users_authentication import require_auth_admin
from models import Refund, Receipt, Sale, Product, CartItem
import uuid


class RefundAPI(MethodView):
    @require_auth_admin
    def get(self):

        refunds_list = [Refund.from_json(r) for r in import_data('./refunds.json')]
        id_filter = request.args.get('id')
        sale_id_filter = request.args.get('sale_id')
        date_filter = request.args.get('date')
        total_filter = request.args.get('total')

        if date_filter:
            try:
                datetime.strptime(date_filter, "%Y-%m-%d")
            except ValueError as ex:
                return jsonify(message='the date must be in this format YEAR-MONTH-DAY'), 400
            
        if id_filter:
            try:
                id_filter = int(id_filter)
            except ValueError as ex:
                return jsonify(message='the id must be an integer'), 400

        if sale_id_filter:
            try:
                sale_id_filter = int(sale_id_filter)
            except ValueError as ex:
                return jsonify(message='the sale id must be an integer'), 400
            
        if total_filter:
            try:
                total_filter = float(total_filter)
            except ValueError as ex:
                return jsonify(message='the total must be a number'), 400

        filtered = refunds_list

        if id_filter:
            filtered = [r for r in filtered if r.id == id_filter]

        if sale_id_filter:
            filtered = [r for r in filtered if r.sale_id == sale_id_filter]

        if date_filter: 
            filtered = [r for r in filtered if r.date == date_filter]
        
        if total_filter:
            filtered = [r for r in filtered if r.total == total_filter]

        return jsonify([r.to_json() for r in filtered])

    @require_auth_admin
    def post(self):

        refunds_list = [Refund.from_json(r, types_map={'products': CartItem}) for r in import_data('./refunds.json')]
        receipts_list = [Receipt.from_json(r, types_map={'products': CartItem}) for r in import_data('./receipts.json')]
        sales_list = [Sale.from_json(s, types_map={'products': CartItem}) for s in import_data('./sales.json')]
        products_list = [Product.from_json(p) for p in import_data('./products.json')]
        request_body = request.json
        code = int(str(uuid.uuid4().int)[:10])


        if 'receipt_code' not in request_body:
            return jsonify(message='receipt_code is require'), 400
        
        if 'products' not in request_body:
            return jsonify(message='products is require'), 400
        
        if not isinstance(request_body['products'], list):
            return jsonify(message='products must be a list'), 400
        
        for product in request_body['products']:
            if not isinstance(product, dict):
                return jsonify(message='each product must be a dictionary with product_id and quantity'), 400
            if not isinstance(product['product_id'], int) or not isinstance(product['quantity'], int):
                return jsonify(message='product_id and quantity must be integers'), 400
        
        user_receipt = next((r for r in receipts_list if r.code == request_body['receipt_code']), None)

        if not user_receipt:
            return jsonify(message='receipt not found'), 404
        
        user_sale = next((s for s in sales_list if s.id == user_receipt.sale_id), None)

        if not user_sale:
            return jsonify(message='sale not found'), 404
        
        refund_items = []
        
        for product in request_body['products']:
            original_product = next((p for p in user_sale.products if product['product_id'] == p.product_id), None)

            if not original_product:
                return jsonify(message='product not found on sale'), 404
            
            if product['quantity'] > original_product.quantity:
                return jsonify(message='refund quantity exceeds purchased quantity'), 400
            
            product_obj = next((p for p in products_list if p.id == product['product_id']), None)
            if not product_obj:
                return jsonify(message='product not found'), 404
            
            to_cart_item = CartItem(CartItem.next_id(refund_items), product['product_id'], product['quantity'])
            refund_items.append(to_cart_item)
            
            product_obj.restock(product['quantity'])

        new_refund = Refund(Refund.next_id(refunds_list), user_sale.id, refund_items, Refund.total_refund(refund_items, products_list))

        refunds_list.append(new_refund)
        user_sale.refund_status = True

        export_data([r.to_json() for r in refunds_list], './refunds.json')
        export_data([s.to_json() for s in sales_list], './sales.json')
        export_data([r.to_json() for r in receipts_list], './receipts.json')
        export_data([p.to_json() for p in products_list], './products.json')

        return jsonify({
            'products': [ri.to_json() for ri in refund_items],
            'refund_date': new_refund.refund_date,
            'total': new_refund.total
        })


def register_api(app):
    refund_view = RefundAPI.as_view('refund_api')
    app.add_url_rule('/refunds', view_func=refund_view, methods=['GET', 'POST'])

