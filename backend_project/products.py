

from flask.views import MethodView
from flask import request, jsonify
from models import Product
from data import export_data, import_data, products_path
import uuid
from users_authentication import require_auth_admin
from utils import error_response, validate_int, validate_date, handle_errors


class ProductAPI(MethodView):
    @handle_errors
    def get(self):
        products_list = [Product.from_json(p) for p in import_data(products_path)]
        id_filter = request.args.get('id')
        name_filter = request.args.get('name')
        code_filter = request.args.get('code')
        entry_date_filter = request.args.get('entry_date')
        brand_filter = request.args.get('brand')
        stock_filter = request.args.get('stock')

        if id_filter:
            id_filter = validate_int(id_filter, 'id')
        
        if stock_filter:
            stock_filter = validate_int(stock_filter, 'stock')

        if code_filter:
            if len(code_filter) != 10:
                raise ValueError('invalid code format')
            
            if not all(c in '0123456789ABCDEF' for c in code_filter):
                raise ValueError('invalid code format')
        
        if entry_date_filter:
            entry_date_filter = validate_date(entry_date_filter)

            
        filtered = products_list

        if id_filter:
            filtered = [p for p in filtered if p.id == id_filter]

        if name_filter:
            filtered = [p for p in filtered if p.name == name_filter]

        if code_filter:
            filtered = [p for p in filtered if p.code == code_filter]

        if entry_date_filter:
            filtered = [p for p in filtered if p.entry_date == entry_date_filter]

        if brand_filter:
            filtered = [p for p in filtered if p.brand == brand_filter]

        if stock_filter:
            filtered = [p for p in filtered if p.stock == stock_filter]
            

        return jsonify([p.to_json() for p in filtered]), 200

    @require_auth_admin
    @handle_errors
    def post(self):
        products_list = [Product.from_json(p) for p in import_data(products_path)]
        code = uuid.uuid4().hex.upper()[:10]
        request_body = request.json

        require_fields = ['name', 'price', 'brand', 'stock']
        for key in request_body.keys():
            if key not in require_fields:
                return error_response(f'unexpected field: {key}', 422)
            
        for key in require_fields:
            if key not in request_body.keys():
                return error_response(f'missing field: {key}', 400)

        price = validate_int(request_body['price'], 'price')
        stock = validate_int(request_body['stock'], 'stock')

        product_check = any(p.name == request_body['name'] for p in products_list)
        code_check = any(p.code == code for p in products_list)

        if not product_check and not code_check:
            new_product = Product(Product.next_id(products_list), code, request_body['name'], price, request_body['brand'], stock)
        
        else:
            return error_response('product already exists', 409)
        
        products_list.append(new_product)
        export_data([p.to_json() for p in products_list], products_path)

        return jsonify(message='product created'), 201


    @require_auth_admin
    @handle_errors
    def patch(self, id):
        products_list = [Product.from_json(p) for p in import_data(products_path)]
        product_to_update = next((p for p in products_list if p.id == id), None)
        request_body = request.json

        if not product_to_update:
            return error_response('product not found', 404)

        allowed_fields = ['name', 'price', 'brand', 'stock']
        for key in request_body.keys():
            if key not in allowed_fields:
                return error_response(f'unexpected field: {key}', 422)
            
        if 'price' in request_body:
            price = validate_int(request_body['price'], 'price')
            if price < 0:
                raise ValueError('price must be a positive number')
            
        if 'stock' in request_body:
            stock = validate_int(request_body['stock'], 'stock')
            if stock < 0:
                raise ValueError('stock must be a positive number')
            
        for key, value in request_body.items():
            if hasattr(product_to_update, key):
                setattr(product_to_update, key, value)

        export_data([p.to_json() for p in products_list], products_path)
        return jsonify(product_to_update.to_json()), 200
        
    
    @require_auth_admin
    @handle_errors
    def delete(self, id):
        products_list = [Product.from_json(p) for p in import_data(products_path)]
        product_to_delete = next((p for p in products_list if p.id == id), None)

        if not product_to_delete:
            return error_response('product not found', 404)

        products_list =[p for p in products_list if p.id != id]
        export_data([p.to_json() for p in products_list], products_path)
        return jsonify(message='product deleted'), 200


def register_api(app):
    products_view = ProductAPI.as_view('product_api')
    app.add_url_rule('/products', view_func=products_view, methods=['GET', 'POST'])
    app.add_url_rule('/products/<int:id>', view_func=products_view, methods=['PATCH', 'DELETE'])