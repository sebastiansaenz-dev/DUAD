from sqlalchemy import select, func
from werkzeug.exceptions import Conflict, BadRequest, NotFound
from .base_repo import BaseRepository
from models import Products


class CategoriesRepo(BaseRepository):
    def __init__(self, model, schema, session=None):
        super().__init__(model, schema, session)

    def get_by_name(self, name):
        stmt = select(self.model).where(self.model.name == name)
        return self.session.execute(stmt).scalars().first()

    def count_products(self, category_id):
        stmt = select(func.count()).select_from(Products).where(Products.category_id == category_id)
        return self.session.execute(stmt).scalar() or 0

    def create_category(self, data):
        name = (data.get('name') or '').strip() if data else ''
        if not name:
            raise BadRequest('name is required')

        if self.get_by_name(name):
            raise Conflict('category already exists')

        return self.create({'name': name})

    def update_category(self, id, data):
        if 'name' not in data:
            return self.update(id, data)

        name = (data.get('name') or '').strip()
        if not name:
            raise BadRequest('name is required')

        existing = self.get_by_name(name)
        if existing and existing.id != id:
            raise Conflict('category already exists')

        return self.update(id, {'name': name})

    def delete_category(self, id):
        item = self.session.get(self.model, id)
        if not item:
            raise NotFound('item not found')

        if self.count_products(id) > 0:
            raise BadRequest('cannot delete a category that still has products')

        return self.delete(id)
