


from .base_repo import BaseRepository
from sqlalchemy import select, func
from models import Categories
import math


class ProductsRepo(BaseRepository):
    def __init__(self, model, schema, session=None):
        super().__init__(model, schema, session)

    def get_or_create_category(self, name):
        category_name = name.strip()
        category = self.session.execute(
            select(Categories).where(Categories.name == category_name)
        ).scalars().first()

        if category:
            return category

        category = Categories(name=category_name)
        self.session.add(category)
        self.session.flush()
        return category

        
    def get_products(self, filters, page=1, per_page=20):

        if filters is None:
            filters = {}
        filters.pop('page', None)
        filters.pop('per_page', None)
        filters.pop('all', None)

        name_search = filters.pop('name', None)
        category_name = filters.pop('category', None)

        valid_filters = self.schema.load(filters, partial=True)

        valid_filters = self.to_dict(valid_filters)
        valid_filters.pop('category', None)
        
        total_stmt = select(func.count()).select_from(self.model).filter_by(**valid_filters)

        if name_search:
            total_stmt = total_stmt.filter(self.model.name.ilike(f"%{name_search}%"))
        if category_name:
            total_stmt = total_stmt.join(self.model.category).filter(Categories.name == category_name)

        total_products = self.session.execute(total_stmt).scalar()
        stmt = select(self.model).filter_by(**valid_filters).order_by(self.model.id)
        if name_search:
            stmt = stmt.filter(self.model.name.ilike(f"%{name_search}%"))
        if category_name:
            stmt = stmt.join(self.model.category).filter(Categories.name == category_name)



        if page is not None and per_page is not None:
            page = int(page)
            per_page = int(per_page)
            offset_value = (page - 1) * per_page
            stmt = stmt.limit(per_page).offset(offset_value)
            total_pages = math.ceil(total_products / per_page) if total_products > 0 else 0
        else:
            page = 1
            per_page = total_products if total_products > 0 else 1
            total_pages = 1

        results = self.session.execute(stmt).scalars().unique().all()

        return {
            'items': self.schema.dump(results, many=True),
            'total_products': total_products,
            'page': page,
            'per_page': per_page,
            'total_pages': total_pages
        }




