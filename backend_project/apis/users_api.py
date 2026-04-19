

from flask.views import MethodView
from flask import jsonify, request
from schemas.users_schema import UsersSchema
from repos.users_repo import UsersRepo
from models import Users
from utils import require_auth, require_admin, handle_errors


class UserAPI(MethodView):

    def __init__(self):
        self.repo = UsersRepo(Users, UsersSchema())


    @require_auth
    @handle_errors
    def get(self, current_user_id):

        user = self.repo.get_by_id(current_user_id)

        return jsonify(user)


    @require_auth
    @handle_errors
    def patch(self, current_user_id):

        data = request.get_json()

        updated_user = self.repo.update(current_user_id, data)

        return jsonify(updated_user)
    
    @require_auth
    @handle_errors
    def delete(self, current_user_id):

        deleted_user = self.repo.delete(current_user_id)

        if deleted_user:
            return jsonify(message='user deleted'), 200
        

class LoginAPI(MethodView):
    def __init__(self):
        self.repo = UsersRepo(Users, UsersSchema())

    @handle_errors
    def post(self):
        data = request.get_json()

        result = self.repo.login_user(data)

        return jsonify({
            'message': 'login successfully',
            'user': result['user'],
            'token': result['token']
        })


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



def register_api(app):
    login_view = LoginAPI.as_view('login_api')
    register_view = RegisterAPI.as_view('register_user_api')
    user_view = UserAPI.as_view('user_api')
    

    app.add_url_rule('/users', view_func=user_view, methods=['GET', 'POST', 'PATCH', 'DELETE'])
    app.add_url_rule('/login', view_func=login_view, methods=['POST'])
    app.add_url_rule('/register-user', view_func=register_view, methods=['POST'])