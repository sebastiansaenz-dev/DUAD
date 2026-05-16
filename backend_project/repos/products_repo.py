


from .base_repo import BaseRepository
from sqlalchemy import select, func
import math


class ProductsRepo(BaseRepository):
    def __init__(self, model, schema, session=None):
        super().__init__(model, schema, session)

        
    def get_products(self, filters, page=1, per_page=20):

        if 'page' in filters:
            filters.pop('page')
        if 'per_page' in filters:
            filters.pop('per_page')

        valid_filters = self.schema.load(filters, partial=True)

        valid_filters = self.to_dict(valid_filters)

        offset_value = (page - 1) * per_page

        stmt = select(self.model).filter_by(**valid_filters).order_by(self.model.id).limit(per_page).offset(offset_value)

        results = self.session.execute(stmt).scalars().all()

        total_stmt = select(func.count()).select_from(self.model).filter_by(**valid_filters)
        total_products = self.session.execute(total_stmt).scalar()

        total_pages = math.ceil(total_products / per_page) if total_products > 0 else 0

        return {
            'items': self.schema.dump(results, many=True),
            'total_products': total_products,
            'page': page,
            'per_page': per_page,
            'total_pages': total_pages
        }




