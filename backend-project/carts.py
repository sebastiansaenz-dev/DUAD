

from flask.views import MethodView
from flask import request, jsonify
from models import Product, CartItem, Cart, User
from data import import_data, export_data, carts_path, users_path, products_path
from users_authentication import require_auth, tokens
from utils import error_response, validate_int, handle_errors


class CartAPI(MethodView):
    @require_auth
    @handle_errors
    def get(self):
        carts_list = [Cart.from_json(c, types_map={'product': CartItem}) for c in import_data(carts_path)]
        users_list = [User.from_json(u) for u in import_data(users_path)]
        products_list = [Product.from_json(p) for p in import_data(products_path)]
        id_filter = request.args.get('id')
        user_id_filter = request.args.get('user_id')
        product_id_filter = request.args.get('product_id')


        token = request.headers.get('Authorization').split()[1]
        current_user = next((u for u in users_list if u.username == tokens[token]), None)

        if not current_user:
            return error_response('invalid token', 401)
        
    
        if current_user.role != 'admin':
            user_cart = next((c for c in carts_list if c.user_id == current_user.id), None)

            if not user_cart:
                return error_response('cart not found', 404)

            return jsonify({
                'cart': user_cart.to_json(),
                'total': user_cart.get_total(products_list)
                }), 200
        
        if id_filter:
            id_filter = validate_int(id_filter, 'id')

        if user_id_filter:
            user_id_filter = validate_int(user_id_filter, 'user_id')

        if product_id_filter:
            product_id_filter = validate_int(product_id_filter, 'product_id')
            
        filtered = carts_list

        if id_filter:
            filtered = [c for c in filtered if c.id == id_filter]

        if user_id_filter:
            filtered = [c for c in filtered if c.user_id == user_id_filter]

        if product_id_filter:
            filtered = [c for c in filtered if any(item.product_id == product_id_filter for item in c.products)]

        return jsonify([c.to_json() for c in filtered]), 200


    @require_auth
    @handle_errors
    def patch(self, id):
        products_list = [Product.from_json(p) for p in import_data(products_path)]
        carts_list = [Cart.from_json(c, types_map={'products': CartItem}) for c in import_data(carts_path)]
        users_list = [User.from_json(u) for u in import_data(users_path)]
        request_body = request.json

        token = request.headers.get('Authorization').split()[1]
        current_user = next((u for u in users_list if u.username == tokens[token]), None)
        current_cart = next((c for c in carts_list if c.user_id == current_user.id), None)

        if not current_user:
            return error_response('invalid token', 401)
        
        if not current_cart:
            return error_response('cart not found', 404)

        for item in request_body:
            if not isinstance(item, dict):
                raise ValueError('invalid item format')
            allowed_keys = {'product_id', 'quantity'}
            if set(item.keys()) != allowed_keys:
                raise ValueError('invalid item format')
        
            if not isinstance(item['product_id'], int):
                raise ValueError('product_id must be an integer')
            
            if not isinstance(item['quantity'], int):
                raise ValueError('quantity must be an integer')
        
        
        if current_user.role != 'admin':
            if current_user.id != id:
                return error_response("cannot modify another user's cart", 403)
        
        cart_items = []
        errors = []
        
        for item in request_body:
            product = next((p for p in products_list if p.id == item['product_id']), None)

            if not product:
                errors.append({'product_id': item['product_id'], 'error': 'product not found'})
                continue
            
            if product.stock < item['quantity']:
                errors.append({'product_id': item['product_id'], 'error': 'insufficient stock'})
                continue

            new_cart_item = CartItem(CartItem.next_id(current_cart.products), product.id, item['quantity'])
            cart_items.append(new_cart_item)

        for item in cart_items:

            existing_cart_item = next((ci for ci in current_cart.products if ci.product_id == item.product_id), None)
            product_obj = next((p for p in products_list if p.id == item.product_id), None)

            if not product_obj:
                return error_response('item not found', 404)

            if existing_cart_item:
                old_quantity = existing_cart_item.quantity
                new_quantity = item.quantity

                if new_quantity == 0:
                    product_obj.restock(old_quantity)
                    current_cart.products.remove(existing_cart_item)

                elif new_quantity < 0:
                    return error_response('quantity must be a positive number', 400)

                else:
                    difference = new_quantity - old_quantity

                    if difference > 0:
                        product_obj.reduce_stock(difference)
                    elif difference < 0:
                        product_obj.restock(abs(difference))

                    existing_cart_item.quantity = new_quantity
            
            else:
                if item.quantity > 0:
                    product_obj.reduce_stock(item.quantity)
                    current_cart.products.append(item)

                else:
                    errors.append({'product_id': item.product_id, 'error': 'not enough stock available', 'stock available': product_obj.stock})
                
        export_data([p.to_json() for p in products_list], products_path)
        export_data([c.to_json() for c in carts_list], carts_path)

        return jsonify({
            'message': 'products added to cart',
            'errors': errors,
            'total': current_cart.get_total(products_list)
        }), 200


    @require_auth
    @handle_errors
    def delete(self, id=None):
        carts_list = [Cart.from_json(c, types_map={'products': CartItem}) for c in import_data(carts_path)]
        products_list = [Product.from_json(p) for p in import_data(products_path)]
        users_list = [User.from_json(u) for u in import_data(users_path)]
        request_body = request.json
        token = request.headers.get('Authorization').split()[1]
        current_user = next((u for u in users_list if u.username == tokens[token]), None)

        if not current_user:
            return error_response('invalid token', 401)

        if id is not None:
            if current_user.role != 'admin':
                return error_response('admin permissions require', 403)                
            current_cart = next((c for c in carts_list if c.id == id), None)

        else:
            current_cart = next((c for c in carts_list if c.user_id == current_user.id), None)
        
        if not current_cart:
            return error_response('cart not found', 404)
        
        for item in request_body:
            if not isinstance(item, dict):
                raise ValueError('invalid item format')
            allowed_fields = {'product_id'}
            if set(item.keys()) != allowed_fields:
                raise ValueError('invalid item format')
            if not isinstance(item['product_id'], int):
                raise ValueError('product_id must be an integer')
            
        products = []
        errors = []

        for item in request_body:
            product = next((p for p in products_list if p.id == item['product_id']), None)

            if not product:
                errors.append({'product_id': {item['product_id']}, 'error': 'product not found'})
                continue

            products.append(product)

        for p in products:
            existing_cart_item = next((ci for ci in current_cart.products if ci.product_id == p.id), None)

            if not existing_cart_item:
                errors.append({'product_id': p.id, 'error': 'product not found'})
                continue
            
            p.restock(existing_cart_item.quantity)
            current_cart.products.remove(existing_cart_item)

        export_data([c.to_json() for c in carts_list], carts_path)
        export_data([p.to_json() for p in products_list], products_path)

        if errors:
            return jsonify({
                'errors': errors,
                'items deleted': [p.id for p in products]
            }), 200
        
        return jsonify(message='item(s) deleted'), 200


def register_api(app):
    carts_view = CartAPI.as_view('carts_api')
    app.add_url_rule('/cart', view_func=carts_view, methods=['GET', 'PATCH', 'DELETE'])
    app.add_url_rule('/cart/<int:id>', view_func=carts_view, methods=['PATCH', 'DELETE'])
