from repos.categories_repo import CategoriesRepo
from models import Categories
from schemas.categories_schema import CategoriesSchema


class CategoryService:
    def __init__(self, repo=None):
        self.repo = repo if repo else CategoriesRepo(Categories, CategoriesSchema())

    def get_all(self, filters=None):
        return self.repo.get_all(filters or {})

    def get_by_id(self, id):
        return self.repo.get_by_id(id)
