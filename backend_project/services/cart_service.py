
from extensions import cache_manager
from repos.carts_repo import CartsRepo
from models import Carts
from schemas.carts_schema import CartsSchema



class CartService:
    def __init__(self, cache=None, repo=None):
        self.cache = cache if cache else cache_manager
        self.repo = repo if repo else CartsRepo(Carts, CartsSchema())

    def get_cart(self, current_user_id):

        cache_key = f"cart:user:{current_user_id}"

        cached_cart = self.cache.get_data(cache_key)

        if cached_cart:
            return cached_cart

        cart = self.repo.get_cart(current_user_id)

        ttl = 18000
        self.cache.store_data(cache_key, cart, ttl)

        return cart

    def add_products(self, user_id, products):
        result = self.repo.add_products(user_id, products)

        self.cache.delete_data(f"cart:user:{user_id}")

        return result

    def update_quantity(self, user_id, products):
        result = self.repo.add_products(user_id, products)

        self.cache.delete_data(f"cart:user:{user_id}")

        return result

    def delete_product(self, user_id, products):
        result = self.repo.delete_product(user_id, products)

        self.cache.delete_data(f"cart:user:{user_id}")

        return result










