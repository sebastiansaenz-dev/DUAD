

from flask.views import MethodView
from flask import jsonify, request, Blueprint, make_response
from schemas.users_schema import UsersSchema
from repos.users_repo import UsersRepo
from models import Users
from utils import require_auth, handle_errors
from flask_jwt_extended import get_jwt, jwt_required


users_bp = Blueprint('users', __name__, url_prefix='/users')

class UserAPI(MethodView):

    def __init__(self):
        self.repo = UsersRepo(Users, UsersSchema())


    @require_auth()
    @handle_errors
    def get(self, current_user_id):

        user = self.repo.get_by_id(current_user_id)

        return jsonify(user)


class LoginAPI(MethodView):
    def __init__(self):
        self.repo = UsersRepo(Users, UsersSchema())

    @handle_errors
    def post(self):
        data = request.get_json()

        result = self.repo.login_user(data)

        return jsonify(result)


class RegisterAPI(MethodView):
    def __init__(self):
        self.repo = UsersRepo(Users, UsersSchema())

    @handle_errors
    def post(self):

        data = request.get_json()

        result = self.repo.register_user(data)

        return jsonify({
            "message": 'user created',
            "user": result['user'],
            "token": result['token']
        })


class LogoutAPI(MethodView):
    def __init__(self):
        self.repo = UsersRepo(Users, UsersSchema())

    @handle_errors
    @jwt_required(refresh=True)
    def post(self):

        token_data = get_jwt()

        result = self.repo.logout_user(token_data)

        if result:
            return jsonify({
                "message": "Logged out"
            })



login_view = LoginAPI.as_view('login_api')
register_view = RegisterAPI.as_view('register_user_api')
user_view = UserAPI.as_view('user_api')
logout_view = LogoutAPI.as_view('logout_api')

users_bp.add_url_rule('/', view_func=user_view, methods=['GET'])
users_bp.add_url_rule('/login', view_func=login_view, methods=['POST'])
users_bp.add_url_rule('/register-user', view_func=register_view, methods=['POST'])
users_bp.add_url_rule('/logout', view_func=logout_view, methods=['POST'])

