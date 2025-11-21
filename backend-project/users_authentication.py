

from flask.views import MethodView
from flask import jsonify, request
import secrets
from data import export_data, import_data, add_item_to_list, check_if_exists
from models import User, Cart


tokens = {}

def require_auth(func):
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify(message='Authorization header missing'), 401

        parts = auth_header.split()
        if len(parts) != 2 or parts[0] != 'Bearer':
            return jsonify(message='Invalid authorization format')
        
        token = parts[1]
        username = tokens.get(token)

        if not username:
            return jsonify(message='invalid token')
        
        request.user = username

        return func(*args, **kwargs)
    return wrapper


def require_auth_admin(func):
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify(message='Authorization header missing'), 401
        
        token = auth_header.split()[-1]
        username = tokens.get(token)
        if not username:
            return jsonify(message='invalid token'), 401
        
        users = [User.from_json(u) for u in import_data('./users.json')]
        user = next((u for u in users if u.username == username), None)

        if not user or user.role != 'admin':
            return jsonify(message='Admin privileges require'), 403
        
        request.user = username

        return func(*args, **kwargs)
    return wrapper


class UserAPI(MethodView):

    @require_auth_admin
    def get(self):
        users_list = [User.from_json(u) for u in import_data('./users.json')]
        id_filter = request.args.get('id')
        username_filter = request.args.get('username')

        if id_filter:
            try:
                id_filter = int(id_filter)
            except:
                return jsonify(message='id must be a integer')
            
        filtered = users_list

        if id_filter:
            filtered = [u for u in filtered if u.id == id_filter]

        if username_filter:
            filtered = [u for u in filtered if u.username == username_filter]

        return jsonify([u.to_json() for u in filtered]), 200
    

    @require_auth
    def patch(self, id):

        users_list = [User.from_json(u) for u in import_data('./users.json')]
        user_to_update = next((user for user in users_list if user.id == id), None)
        request_body = request.json

        token = request.headers.get('Authorization').split()[1]
        current_user = next((u for u in users_list if u.username == tokens[token]), None)

        if not current_user:
            return jsonify(message='invalid token'), 401
        
        if not user_to_update:
            return jsonify(message='missing user_to_update id')

        
        if current_user.role != 'admin':
            if current_user.id != id:
                return jsonify(message='cannot modified other users'), 403
            
            allowed_fields = ['username', 'password']
            for key in request_body.keys():
                if key not in allowed_fields:
                    return jsonify(message=f'{key} cannot be modified'), 403
        
        else:
            if 'id' in request_body:
                return jsonify(message='id cant be modified'), 400
        

        if 'username' in request_body:
            temporal_user = User(None, request_body['username'], None)
            if User.exists_in_list(temporal_user, users_list, 'username'):
                return jsonify(message='username already exists, please choose another')

        for key, value in request_body.items():
            if hasattr(user_to_update, key):
                setattr(user_to_update, key, value)

        export_data([u.to_json() for u in users_list], './users.json')
        return jsonify(user_to_update.to_json()), 200
    
    
    @require_auth
    def delete(self, id):
        users_list = [User.from_json(u) for u in import_data('./users.json')]
        user_to_delete = next((u for u in users_list if u.id == id), None)

        token = request.headers.get('Authorization').split()[1]
        current_user = next((u for u in users_list if u.username == tokens[token]), None)

        if not user_to_delete:
            return jsonify(message='user not found'), 404
        
        if current_user.role != 'admin' and current_user.id != id:
            return jsonify(message='cannot delete other user'), 403
            
        users_list = [u for u in users_list if u.id != id]
        export_data([u.to_json() for u in users_list], './users.json')

        return jsonify(message='user deleted'), 200


class LoginAPI(MethodView):

    def post(self):
        try:
            users_list = [User.from_json(u) for u in import_data('./users.json')]
            print(users_list)
            request_body = request.json

            if 'username' not in request_body:
                raise ValueError('username missing')
            
            if 'password' not in request_body:
                raise ValueError('password missing')
            
            username = request_body['username']
            password = request_body['password']

            for user in users_list:
                if username == user.username and password == user.password:
                    token = secrets.token_hex(16)
                    tokens[token] = username
                    return jsonify(token=token)
            
            else:
                return jsonify(message='invalid username or password'), 400
        
        except ValueError as ex:
            return jsonify(message='there was an error')
        except Exception as ex:
            return jsonify(message='there was an error')


class RegisterUserAPI(MethodView):

    def post(self):
        try:

            users_list = [User.from_json(u) for u in import_data('./users.json')]
            carts_list = [Cart.from_json(c) for c in import_data('./carts.json')]
            request_body = request.json

            if 'username' not in request_body:
                raise ValueError('username missing')
            
            if 'password' not in request_body:
                raise ValueError('password missing')
            
            username = request_body['username']
            password = request_body['password']
            
            temporal_user = User(None, username, password)
            
            user_check = User.exists_in_list(temporal_user, users_list, 'username')

            if not user_check:
                new_user = User(User.next_id(users_list), username, password)
                new_cart = Cart(Cart.next_id(carts_list), new_user.id)

                users_list.append(new_user)
                carts_list.append(new_cart)

                export_data([user.to_json() for user in users_list], './users.json')
                export_data([cart.to_json() for cart in carts_list], './carts.json')

                return jsonify(message='user registered'), 200
            
            else:
                return jsonify(message='username already exists, please use another username'), 400


        except ValueError as ex:
            print(ex)
            return jsonify(message='there was an error'), 400
        except Exception as ex:
            print(ex)
            return jsonify(message='there was an error'), 400


def register_api(app):
    login_view = LoginAPI.as_view('login_api')
    register_view = RegisterUserAPI.as_view('register_user_api')
    user_view = UserAPI.as_view('user_api')
    

    app.add_url_rule('/users', view_func=user_view, methods=['GET'])
    app.add_url_rule('/users/<int:id>', view_func=user_view, methods=['PATCH', 'DELETE'])
    app.add_url_rule('/login', view_func=login_view, methods=['POST'])
    app.add_url_rule('/register-user', view_func=register_view, methods=['POST'])