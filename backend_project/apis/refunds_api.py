


from flask import request, jsonify, Blueprint
from flask.views import MethodView
from services.refund_service import RefundService
from utils import require_auth, handle_errors

refunds_bp = Blueprint('refunds', __name__, url_prefix='/refunds')

class RefundsAPI(MethodView):

    def __init__(self):
        self.service = RefundService()
    
    @require_auth
    @handle_errors
    def get(self, current_user_id):

        refunds = self.service.get_refunds(current_user_id)

        return jsonify(refunds)
    
    @require_auth
    @handle_errors
    def post(self, current_user_id):

        data = request.get_json()
        new_refund = self.service.create_refund(current_user_id, data)

        return jsonify(self.repo.schema.dump(new_refund))

refund_view = RefundsAPI.as_view('refund_api')
refunds_bp.add_url_rule('/refunds', view_func=refund_view, methods=['GET', 'POST'])



