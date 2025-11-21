



from flask.views import MethodView
from flask import request, jsonify
from models import Product
from data import export_data, import_data, add_item_to_list, check_if_exists
from datetime import datetime
import uuid
from users_authentication import require_auth, tokens, require_auth_admin



class ProductAPI(MethodView):
    def get(self):
        products_list = [Product.from_json(p) for p in import_data('./products.json')]
        id_filter = request.args.get('id')
        name_filter = request.args.get('name')
        code_filter = request.args.get('code')
        entry_date_filter = request.args.get('entry_date')
        brand_filter = request.args.get('brand')
        stock_filter = request.args.get('stock')


        if id_filter:
            try:
                id_filter = int(id_filter)
            except ValueError as ex:
                return jsonify(message='id must be an integer'), 400
            
        if stock_filter:
            try:
                stock_filter = int(stock_filter)
            except ValueError as ex:
                return jsonify(message='stock must be a integer'), 400
            
        if code_filter:
                if not code_filter.isalnum():
                    return jsonify(message='code must be alphanumeric'), 400
                
                if any(char.isalpha() and not char.isupper() for char in code_filter):
                    return jsonify(message='letters must be in uppercase'), 400
        
        if entry_date_filter:
            try:
                datetime.strptime(entry_date_filter, "%Y-%m-%d")
            except (ValueError, TypeError):
                return jsonify(message='the date must be in this format YYYY-MM-DD'), 400
            

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
    def post(self):
        try:
            products_list = [Product.from_json(p) for p in import_data('./products.json')]
            code = uuid.uuid4().hex.upper()[:10]
            request_body = request.json

            require_fields = ['name', 'price', 'brand', 'stock']
            for key in request_body.keys():
                if key not in require_fields:
                    return jsonify(message=f'unexpected key: {key}')
                
            require_fields = ['name', 'price', 'brand', 'stock']
            for key in require_fields:
                if key not in request_body.keys():
                    return jsonify(message=f'{key} missing in the body')
                
            try:          
                price = float(request_body['price'])
                stock = int(request_body['stock'])
            except ValueError as ex:
                print(ex)
                return jsonify(message='price must be a float and stock an integer'), 400
                

            product_check = any(p.name == request_body['name'] for p in products_list)

            if not product_check:
                new_product = Product(Product.next_id(products_list), code, request_body['name'], price, request_body['brand'], stock)
            
            else:
                return jsonify(message='product already exists'), 400
            
            products_list.append(new_product)
            export_data([p.to_json() for p in products_list], './products.json')

            return jsonify(message='product created'), 200
        
        except Exception as ex:
            print(ex)
            return jsonify(message='there was an error'), 500



    @require_auth_admin
    def patch(self, id):
        try:

            products_list = [Product.from_json(p) for p in import_data('./products.json')]
            product_to_update = next((p for p in products_list if p.id == id), None)
            request_body = request.json

            allowed_fields = ['name', 'price', 'entry_date', 'brand', 'stock']
            for key in request_body.keys():
                if key not in allowed_fields:
                    return jsonify(message=f'{key} cannot be modified'), 400
                
            if 'entry_date' in request_body:
                try:
                    datetime.strptime(request_body['entry_date'], "%Y-%m-%d")
                except ValueError:
                    return jsonify(message='the entry_date must be in YYYY-MM-DD format'), 400
                
            if 'price' in request_body:
                try:
                    price = float(request_body['price'])
                    if price < 0:
                        return jsonify(message='price must be a positive number')
                except (ValueError, TypeError):
                    return jsonify(message='price must be a number')
                
            if 'stock' in request_body:
                try:
                    stock = float(request_body['stock'])
                    if stock < 0:
                        return jsonify(message='stock must be a positive number')
                    
                except (ValueError, TypeError):
                    return jsonify(message='stock must be a number')
                
            for key, value in request_body.items():
                if hasattr(product_to_update, key):
                    setattr(product_to_update, key, value)

            export_data([p.to_json() for p in products_list], './products.json')
            return jsonify(product_to_update.to_json()), 200


        except Exception as ex:
            print(ex)
            return jsonify(message='there was an error'), 500
            
    
    @require_auth_admin
    def delete(self, id):
        try:

            products_list = [Product.from_json(p) for p in import_data('./products.json')]

            product_to_delete = next((p for p in products_list if p.id == id), None)

            if not product_to_delete:
                return jsonify(message='product not found'), 404

            products_list =[p for p in products_list if p.id != id]
            export_data([p.to_json() for p in products_list], './products.json')
            return jsonify(message='product deleted'), 200

        except Exception as ex:
            print(ex)
            return jsonify(message='there was an error'), 500



def register_api(app):
    products_view = ProductAPI.as_view('product_api')
    app.add_url_rule('/products', view_func=products_view, methods=['GET', 'POST'])
    app.add_url_rule('/products/<int:id>', view_func=products_view, methods=['PATCH', 'DELETE'])