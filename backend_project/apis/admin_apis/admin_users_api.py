

from flask.views import MethodView
from flask import jsonify, request, Blueprint
from schemas.users_schema import UsersSchema
from repos.admin_repos.admin_users_repo import AdminUsersRepo
from models import Users
from utils import require_admin, handle_errors


admin_users_bp = Blueprint('admin_users', __name__, url_prefix='/staff-portal/users')

class AdminUserAPI(MethodView):

    def __init__(self):
        self.repo = AdminUsersRepo(Users, UsersSchema())


    @require_admin
    @handle_errors
    def get(self):

        filters = request.args

        users = self.repo.get_all(filters)

        return jsonify(users)
    

    @require_admin
    @handle_errors
    def post(self):
        data = request.get_json()

        new_user = self.repo.register_user(data)

        return jsonify(new_user)


    @require_admin
    @handle_errors
    def patch(self, id):

        data = request.get_json()

        updated_user = self.repo.update_user(id, data)

        return jsonify(updated_user)

    

    @require_admin
    @handle_errors
    def delete(self, id):

        deleted_user = self.repo.delete_user(id)

        if deleted_user:
            return jsonify(message='user deleted'), 200
        

admin_user_view = AdminUserAPI.as_view('admin_user_api')
admin_users_bp.add_url_rule('/', view_func=admin_user_view, methods=['GET', 'POST'])
admin_users_bp.add_url_rule('/<int:id>', view_func=admin_user_view, methods=['PATCH', 'DELETE'])

