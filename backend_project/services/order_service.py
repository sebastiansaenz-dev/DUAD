

from models import Orders, Carts
from sqlalchemy import select
from schemas.orders_schema import OrdersSchema
from repos.orders_repo import OrdersRepo
from extensions import cache_manager
from constants import CartsStatusEnum
from werkzeug.exceptions import Conflict


class OrderService:
    def __init__(self, cache=None, repo=None):
        self.cache = cache if cache else cache_manager
        self.repo = repo if repo else OrdersRepo(Orders, OrdersSchema())

    def create_order(self, user_id):

        new_order = self.repo.proceed_order(user_id)
        clear_pages = False

        for item in new_order.items:
            self.cache.delete_data(f'products:{item.product_id}')

            if item.product.stock < 5:
                clear_pages = True

        if clear_pages:
            self.cache.delete_data_with_pattern('products:p*')

        return new_order




