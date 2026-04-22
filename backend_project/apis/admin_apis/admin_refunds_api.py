


from flask import request, jsonify, Blueprint
from flask.views import MethodView
from models import Refunds
from schemas.refunds_schema import RefundsSchema
from repos.admin_repos.admin_refunds_repo import AdminRefundsRepo
from utils import require_admin, handle_errors

admin_refunds_bp = Blueprint('admin_refunds', __name__, url_prefix='/staff-portal/refunds')

class AdminRefundsAPI(MethodView):

    def __init__(self):
        self.repo = AdminRefundsRepo(Refunds, RefundsSchema())
    

    @require_admin
    @handle_errors
    def get(self):
        filters = request.args

        refunds = self.repo.get_all(filters)
        return jsonify(refunds)
    

    @require_admin
    @handle_errors
    def post(self, id):

        data = request.get_json()

        new_refund = self.repo.create_refund(id, data)
        return jsonify(new_refund)


admin_refund_view = AdminRefundsAPI.as_view('admin_refund_api')
admin_refunds_bp.add_url_rule('/', view_func=admin_refund_view, methods=['GET', 'POST'])







