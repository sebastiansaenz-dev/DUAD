

from flask.views import MethodView
from flask import request, jsonify
from models import Product, CartItem, Cart, User
from data import import_data, export_data
from users_authentication import require_auth, tokens


class CartAPI(MethodView):
    @require_auth
    def get(self):

        carts_list = [Cart.from_json(c) for c in import_data('./carts.json')]
        users_list = [User.from_json(u) for u in import_data('./users.json')]
        products_list = [Product.from_json(p) for p in import_data('./products.json')]
        id_filter = request.args.get('id')
        user_id_filter = request.args.get('user_id')
        product_id_filter = request.args.get('product_id')


        token = request.headers.get('Authorization').split()[1]
        current_user = next((u for u in users_list if u.username == tokens[token]), None)

        if not current_user:
            return jsonify(message='invalid token'), 400
        
    
        if current_user.role != 'admin':
            user_cart = next((c for c in carts_list if c.user_id == current_user.id), None)

            if not user_cart:
                return jsonify(message='cart not found'), 404

            return jsonify({
                'cart': user_cart.to_json(),
                'total': user_cart.get_total(products_list)
                }), 200
        
        if id_filter:
            try:
                id_filter = int(id_filter)
            except ValueError as ex:
                return jsonify(message='id must be a integer'), 400
            
        if user_id_filter:
            try:
                user_id_filter = int(user_id_filter)
            except ValueError as ex:
                return jsonify(message='user_id must be a integer'), 400
            
        if product_id_filter:
            try:
                product_id_filter = int(product_id_filter)
            except ValueError as ex:
                return jsonify(message='product_id must be a integer'), 400
            
        filtered = carts_list

        if id_filter:
            filtered = [c for c in filtered if c.id == id_filter]

        if user_id_filter:
            filtered = [c for c in filtered if c.user_id == user_id_filter]

        if product_id_filter:
            filtered = [c for c in filtered if any(item.product_id == product_id_filter for item in c.products)]

        return jsonify([c.to_json() for c in filtered]), 200
        


    @require_auth
    def patch(self, id):
        try:

            products_list = [Product.from_json(p) for p in import_data('./products.json')]
            carts_list = [Cart.from_json(c, types_map={'products': CartItem}) for c in import_data('./carts.json')]
            users_list = [User.from_json(u) for u in import_data('./users.json')]
            request_body = request.json

            token = request.headers.get('Authorization').split()[1]
            current_user = next((u for u in users_list if u.username == tokens[token]), None)
            current_cart = next((c for c in carts_list if c.user_id == current_user.id), None)

            if not current_user:
                return jsonify(message='invalid token'), 400
            
            if not current_cart:
                return jsonify(message='cart not found'), 404
            

            for item in request_body:
                if not isinstance(item, dict):
                    raise ValueError('Each item must be a dictionary with product_id and quantity')
                allowed_keys = {'product_id', 'quantity'}
                if set(item.keys()) != allowed_keys:
                    raise ValueError('Item must have product_id and quantity')
            
                if not isinstance(item['product_id'], int) or not isinstance(item['quantity'], int):
                    raise ValueError('product_id and quantity must be integers') 
            
            
            if current_user.role != 'admin':
                if current_user.id != id:
                    return jsonify(message='cannot modified another cart'), 400
            

            cart_items = []
            errors = []
            
            for item in request_body:
                product = next((p for p in products_list if p.id == item['product_id']), None)

                if not product:
                    errors.append({'product_id': item['product_id'], 'error': 'Product not found'})
                    continue
                
                if product.stock < item['quantity']:
                    errors.append({'product_id': item['product_id'], 'error': f'not enough stock available, stock available {product.stock}'})
                    continue

                new_cart_item = CartItem(CartItem.next_id(current_cart.products), product.id, item['quantity'])
                cart_items.append(new_cart_item)

            for item in cart_items:

                existing_cart_item = next((ci for ci in current_cart.products if ci.product_id == item.product_id), None)

                product_obj = next((p for p in products_list if p.id == item.product_id), None)

                if not product_obj:
                    raise ValueError(f"product with id:{item.product_id} doesn't exists")

                if existing_cart_item:
                    old_quantity = existing_cart_item.quantity
                    new_quantity = item.quantity

                    if new_quantity == 0:
                        product_obj.restock(old_quantity)
                        current_cart.products.remove(existing_cart_item)

                    elif new_quantity < 0:
                        raise ValueError('quantity must be a positive integer')

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
                        errors.append({'product_id': item['product_id'], 'error': 'not enough stock available', 'stock available': product_obj.stock})
                    
            export_data([p.to_json() for p in products_list], './products.json')
            export_data([c.to_json() for c in carts_list], './carts.json')

            return jsonify({
                'message': 'products added to cart',
                'errors': errors,
                'total': current_cart.get_total(products_list)
            })

        except ValueError as ex:
            print(ex)
            return jsonify({'error': str(ex)}), 400
        except Exception as ex:
            print(ex)
            return jsonify('there was an error'), 500


    @require_auth
    def delete(self, id=None):
        try:

            carts_list = [Cart.from_json(c, types_map={'products': CartItem}) for c in import_data('./carts.json')]
            products_list = [Product.from_json(p) for p in import_data('./products.json')]
            users_list = [User.from_json(u) for u in import_data('./users.json')]
            request_body = request.json
            token = request.headers.get('Authorization').split()[1]
            current_user = next((u for u in users_list if u.username == tokens[token]), None)

            if not current_user:
                return jsonify(message='invalid token'), 400

            if id is not None:
                if current_user.role != 'admin':
                    return jsonify(message='forbidden'), 403
                
                current_cart = next((c for c in carts_list if c.id == id), None)

            else:
                current_cart = next((c for c in carts_list if c.user_id == current_user.id), None)

            
            if not current_cart:
                return jsonify(message='cart not found')
            
            for item in request_body:
                if not isinstance(item, dict):
                    return jsonify(message='Each item must be a dictionary with product_id')
                allowed_fields = {'product_id'}
                if set(item.keys()) != allowed_fields:
                    raise ValueError('item must have product_id')
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
                    errors.append({'product_id': p.id, 'error': 'product not in cart'})
                    continue
                

                p.restock(existing_cart_item.quantity)
                current_cart.products.remove(existing_cart_item)

            export_data([c.to_json() for c in carts_list], './carts.json')
            export_data([p.to_json() for p in products_list], './products.json')

            if errors:
                return jsonify({
                    'errors': errors,
                    'items deleted': [p.id for p in products]
                })
            
            return jsonify(message='item(s) deleted')


        except ValueError as ex:
            print(ex)
            return jsonify(message=f'error: {ex}'), 400

        except Exception as ex:
            print(ex)
            return jsonify(message='there was an error'), 500


def register_api(app):
    carts_view = CartAPI.as_view('carts_api')
    app.add_url_rule('/cart', view_func=carts_view, methods=['GET', 'PATCH', 'DELETE'])
    app.add_url_rule('/cart/<int:id>', view_func=carts_view, methods=['PATCH', 'DELETE'])


