

from flask.views import MethodView
from flask import request, jsonify
from data import import_data, export_data, refunds_path, receipts_path, sales_path, products_path
from users_authentication import require_auth_admin
from models import Refund, Receipt, Sale, Product, CartItem
import uuid
from utils import error_response, validate_int, validate_date, handle_errors


class RefundAPI(MethodView):
    @require_auth_admin
    @handle_errors
    def get(self):
        refunds_list = [Refund.from_json(r) for r in import_data(refunds_path)]
        id_filter = request.args.get('id')
        sale_id_filter = request.args.get('sale_id')
        date_filter = request.args.get('date')
        total_filter = request.args.get('total')

        if id_filter:
            id_filter = validate_int(id_filter, 'id')
        
        if date_filter:
            date_filter = validate_date(date_filter, 'date')

        if sale_id_filter:
            sale_id_filter = validate_int(sale_id_filter, 'sale_id')

        if total_filter:
            total_filter = validate_int(total_filter, 'total')

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
    @handle_errors
    def post(self):

        refunds_list = [Refund.from_json(r, types_map={'products': CartItem}) for r in import_data(refunds_path)]
        receipts_list = [Receipt.from_json(r, types_map={'products': CartItem}) for r in import_data(receipts_path)]
        sales_list = [Sale.from_json(s, types_map={'products': CartItem}) for s in import_data(sales_path)]
        products_list = [Product.from_json(p) for p in import_data(products_path)]
        request_body = request.json
        code = int(str(uuid.uuid4().int)[:10])


        if 'receipt_code' not in request_body:
            return error_response('missing field: receipt_code', 400)
        
        if 'products' not in request_body:
            return error_response('missing field: products', 400)
        
        if not isinstance(request_body['products'], list):
            raise ValueError('invalid products format')
        
        for product in request_body['products']:
            if not isinstance(product, dict):
                raise ValueError('invalid products format')
            if not isinstance(product['product_id'], int):
                raise ValueError('product_id must be an integer')
            if not isinstance(product['quantity'], int):
                raise ValueError('quantity must be an integer')
        
        user_receipt = next((r for r in receipts_list if r.code == request_body['receipt_code']), None)

        if not user_receipt:
            return error_response('receipt not found', 404)
        
        user_sale = next((s for s in sales_list if s.id == user_receipt.sale_id), None)

        if not user_sale:
            return error_response('sale not found', 404)
        
        refund_items = []
        
        for product in request_body['products']:
            original_product = next((p for p in user_sale.products if product['product_id'] == p.product_id), None)

            if not original_product:
                return error_response('product not found', 404)
            
            if product['quantity'] > original_product.quantity:
                raise ValueError('refund quantity exceeds purchase quantity')
            
            product_obj = next((p for p in products_list if p.id == product['product_id']), None)
            if not product_obj:
                return error_response('product not found', 404)
            
            to_cart_item = CartItem(CartItem.next_id(refund_items), product['product_id'], product['quantity'])
            refund_items.append(to_cart_item)
            
            product_obj.restock(product['quantity'])

        new_refund = Refund(Refund.next_id(refunds_list), user_sale.id, refund_items, Refund.total_refund(refund_items, products_list))

        refunds_list.append(new_refund)
        user_sale.refund_status = True

        export_data([r.to_json() for r in refunds_list], refunds_path)
        export_data([s.to_json() for s in sales_list], sales_path)
        export_data([r.to_json() for r in receipts_list], receipts_path)
        export_data([p.to_json() for p in products_list], products_path)

        return jsonify({
            'products': [ri.to_json() for ri in refund_items],
            'refund_date': new_refund.refund_date,
            'total': new_refund.total
        })


def register_api(app):
    refund_view = RefundAPI.as_view('refund_api')
    app.add_url_rule('/refunds', view_func=refund_view, methods=['GET', 'POST'])

