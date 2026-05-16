


from flask.views import MethodView
from flask import jsonify, Blueprint
from schemas.users_schema import UsersSchema
from repos.users_repo import UsersRepo
from models import Users
from utils import handle_errors
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt, create_access_token


refresh_bp = Blueprint('refresh', __name__, url_prefix='/refresh')

class RefreshAPI(MethodView):

    def __init__(self):
        self.repo = UsersRepo(Users, UsersSchema())


    @handle_errors
    @jwt_required(refresh=True)
    def post(self):

        current_user_id = get_jwt_identity()

        claims = get_jwt()
        additional_claims = {"roles": claims.get("roles", [])}

        new_access_token = create_access_token(
            identity=current_user_id,
            additional_claims=additional_claims,
            fresh=False
        )

        return jsonify({
            "access_token": new_access_token
        })


tokens_view = RefreshAPI.as_view('refresh_api')

refresh_bp.add_url_rule('/', view_func=tokens_view, methods=['POST'])









