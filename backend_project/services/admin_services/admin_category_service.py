from extensions import cache_manager
from services.category_service import CategoryService


class AdminCategoryService(CategoryService):
    def __init__(self, cache=None, repo=None):
        super().__init__(repo=repo)
        self.cache = cache if cache else cache_manager

    def create_category(self, data):
        return self.repo.create_category(data)

    def update_category(self, id, data):
        updated_item = self.repo.update_category(id, data)
        self.cache.delete_data_with_pattern("products:*")
        return updated_item

    def delete_category(self, id):
        deleted_item = self.repo.delete_category(id)
        self.cache.delete_data_with_pattern("products:*")
        return deleted_item
