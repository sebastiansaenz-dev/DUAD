

from extensions import cache_manager
from repos.refunds_repo import RefundsRepo
from models import Refunds
from schemas.refunds_schema import RefundsSchema



class RefundService:
    def __init__(self, repo=None):
        self.repo = repo if repo else RefundsRepo(model=Refunds, schema=RefundsSchema())


    def get_refunds(self, user_id):
        user_refunds = self.repo.get_all({'user_id': user_id})

        return user_refunds


    def create_refund(self, user_id, data):
        new_refund = self.repo.proceed_refund(user_id, data)

        return new_refund
    

