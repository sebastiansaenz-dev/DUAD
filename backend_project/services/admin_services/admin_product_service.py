
from extensions import cache_manager
from repos.products_repo import ProductsRepo
from models import Products
from schemas.products_schema import ProductsSchema
from utils import generate_filters_hash
import uuid



class AdminProductService:
    def __init__(self, cache=None, repo=None):
        self.cache = cache if cache else cache_manager
        self.repo = repo if repo else ProductsRepo(Products, ProductsSchema())

    def get(self, page, per_page, filters=None, id=None):

        if id:
            product = self.cache.get_data(f'products:{id}')
            if product:
                return product
            product = self.repo.get_by_id(id)
            self.cache.store_data(f'products:{id}', product, time_to_live=3600)
            return product

        cache_key = (f"products:p{page}:pp{per_page}")

        if filters:
            filters_hash = generate_filters_hash(filters)
            cache_key += f"f-{filters_hash}"        

        cached_products = self.cache.get_data(cache_key)
        if cached_products:
            return cached_products

        products = self.repo.get_products(filters, page, per_page)

        ttl = 300 if filters else 600

        self.cache.store_data(cache_key, products, time_to_live=ttl)

        return products
    
    def create_product(self, data):

        sku = uuid.uuid4().hex.upper()[:10]

        data['sku'] = sku

        new_item = self.repo.create(data)

        self.cache.delete_data_with_pattern("products:p*:pp*")

        return new_item
    
    def update_product(self, id, data):

        updated_item = self.repo.update(id, data)

        self.cache.delete_data(f"products:{id}")

        self.cache.delete_data_with_pattern("products:p*:pp*")

        return updated_item
    
    def delete_product(self, id):

        deleted_item = self.repo.delete(id)

        self.cache.delete_data(f"products:{id}")

        self.cache.delete_data_with_pattern("products:p*:pp*")

        return deleted_item













