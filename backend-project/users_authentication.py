

from flask.views import MethodView
from flask import jsonify, request
import secrets
from data import export_data, import_data, users_path, carts_path
from models import User, Cart, CartItem
from utils import error_response, validate_int, handle_errors

tokens = {}

def require_auth(func):
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return error_response('Authorization header missing', 401)

        parts = auth_header.split()
        if len(parts) != 2 or parts[0] != 'Bearer':
            return error_response('invalid authorization format', 400)
        
        token = parts[1]
        username = tokens.get(token)

        if not username:
            return error_response('invalid token', 401)
        
        request.user = username

        return func(*args, **kwargs)
    return wrapper


def require_auth_admin(func):
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return error_response('Authorization header missing', 401)
        
        token = auth_header.split()[-1]
        username = tokens.get(token)
        if not username:
            return error_response('invalid token', 401)
        
        users = [User.from_json(u) for u in import_data(users_path)]
        user = next((u for u in users if u.username == username), None)

        if not user or user.role != 'admin':
            return error_response('admin privileges required', 403)
        
        request.user = username

        return func(*args, **kwargs)
    return wrapper


class UserAPI(MethodView):

    @require_auth_admin
    @handle_errors
    def get(self):
        users_list = [User.from_json(u) for u in import_data(users_path)]
        id_filter = request.args.get('id')
        username_filter = request.args.get('username')

        if id_filter:
            id_filter = validate_int(id_filter, 'id')
            
        filtered = users_list

        if id_filter:
            filtered = [u for u in filtered if u.id == id_filter]

        if username_filter:
            filtered = [u for u in filtered if u.username == username_filter]

        return jsonify([u.to_json() for u in filtered]), 200
    
    @require_auth
    @handle_errors
    def patch(self, id):
        users_list = [User.from_json(u) for u in import_data(users_path)]
        user_to_update = next((user for user in users_list if user.id == id), None)
        request_body = request.json

        token = request.headers.get('Authorization').split()[1]
        current_user = next((u for u in users_list if u.username == tokens[token]), None)

        if not current_user:
            return error_response('invalid token', 401)
        
        if not user_to_update:
            return error_response('user_to_update not found', 400)

        
        if current_user.role != 'admin':
            if current_user.id != id:
                return error_response('cannot modify other users', 403)
            
            allowed_fields = ['username', 'password']
            for key in request_body.keys():
                if key not in allowed_fields:
                    return error_response(f'unexpected field: {key}', 403)
        
        else:
            if 'id' in request_body:
                return error_response('unexpected field: id', 400)
        

        if 'username' in request_body:
            temporal_user = User(None, request_body['username'], None)
            if User.exists_in_list(temporal_user, users_list, 'username'):
                return error_response('username already exists', 409)

        for key, value in request_body.items():
            if hasattr(user_to_update, key):
                setattr(user_to_update, key, value)

        export_data([u.to_json() for u in users_list], users_path)
        return jsonify(user_to_update.to_json()), 200
    
    
    @require_auth
    @handle_errors
    def delete(self, id):
        users_list = [User.from_json(u) for u in import_data(users_path)]
        carts_list = [Cart.from_json(c, types_map={'products': CartItem}) for c in import_data(carts_path)]
        user_to_delete = next((u for u in users_list if u.id == id), None)

        token = request.headers.get('Authorization').split()[1]
        current_user = next((u for u in users_list if u.username == tokens[token]), None)

        if not current_user:
            return error_response('user not found', 404)

        current_cart = next((c for c in carts_list if c.user_id == current_user.id), None)

        if not current_cart:
            return error_response('cart not found', 404)

        if not user_to_delete:
            return error_response('user_to_delete not found', 404)
        
        if current_user.role != 'admin' and current_user.id != id:
            return error_response('cannot modify other users', 403)
            
        users_list = [u for u in users_list if u.id != id]
        carts_list = [c for c in carts_list if c.user_id != current_user.id]
        export_data([u.to_json() for u in users_list], users_path)
        export_data([c.to_json() for c in carts_list], carts_path)

        return jsonify(message='user deleted'), 200


class LoginAPI(MethodView):
    @handle_errors
    def post(self):
        users_list = [User.from_json(u) for u in import_data(users_path)]
        print(users_list)
        request_body = request.json

        if 'username' not in request_body:
            return error_response('missing field: username', 400)
        
        if 'password' not in request_body:
            return error_response('missing field: password', 400)
        
        username = request_body['username']
        password = request_body['password']

        for user in users_list:
            if username == user.username and password == user.password:
                token = secrets.token_hex(16)
                tokens[token] = username
                return jsonify(token=token), 200
        
        else:
            raise ValueError('invalid username or password')


class RegisterUserAPI(MethodView):
    @handle_errors
    def post(self):
            users_list = [User.from_json(u) for u in import_data(users_path)]
            carts_list = [Cart.from_json(c) for c in import_data(carts_path)]
            request_body = request.json

            if 'username' not in request_body:
                return error_response('missing field: username', 400)
            
            if 'password' not in request_body:
                return error_response('missing field: password', 400)
            
            username = request_body['username']
            password = request_body['password']
            
            temporal_user = User(None, username, password)
            
            user_check = User.exists_in_list(temporal_user, users_list, 'username')

            if not user_check:
                new_user = User(User.next_id(users_list), username, password)
                new_cart = Cart(Cart.next_id(carts_list), new_user.id)

                users_list.append(new_user)
                carts_list.append(new_cart)

                export_data([user.to_json() for user in users_list], users_path)
                export_data([cart.to_json() for cart in carts_list], carts_path)

                return jsonify(message='user registered'), 200
            
            else:
                return error_response('username already exists', 409)


def register_api(app):
    login_view = LoginAPI.as_view('login_api')
    register_view = RegisterUserAPI.as_view('register_user_api')
    user_view = UserAPI.as_view('user_api')
    

    app.add_url_rule('/users', view_func=user_view, methods=['GET'])
    app.add_url_rule('/users/<int:id>', view_func=user_view, methods=['PATCH', 'DELETE'])
    app.add_url_rule('/login', view_func=login_view, methods=['POST'])
    app.add_url_rule('/register-user', view_func=register_view, methods=['POST'])