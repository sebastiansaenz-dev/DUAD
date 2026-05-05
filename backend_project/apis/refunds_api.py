


from flask import request, jsonify, Blueprint
from flask.views import MethodView
from models import Refunds
from schemas.refunds_schema import RefundsSchema
from repos.refunds_repo import RefundsRepo
from utils import require_auth, handle_errors

refunds_bp = Blueprint('refunds', __name__, url_prefix='/refunds')

class RefundsAPI(MethodView):

    def __init__(self):
        self.repo = RefundsRepo(Refunds, RefundsSchema())
    
    @require_auth
    @handle_errors
    def get(self, current_user_id):

        refunds = self.repo.get_all({'user_id': current_user_id})
        return jsonify(refunds)
    
    @require_auth
    @handle_errors
    def post(self, current_user_id):

        data = request.get_json()

        new_refund = self.repo.create_refund(current_user_id, data)
        return jsonify(self.repo.schema.dump(new_refund))

refund_view = RefundsAPI.as_view('refund_api')
refunds_bp.add_url_rule('/refunds', view_func=refund_view, methods=['GET', 'POST'])



