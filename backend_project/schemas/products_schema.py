from models import Products
from extensions import ma, db


class ProductsSchema(ma.SQLAlchemyAutoSchema):
    category = ma.Function(
        lambda obj: obj.category.name if obj.category else None
    )

    class Meta:
        model = Products
        load_instance = True
        include_fk = True
        sqla_session = db.session

        id = ma.auto_field(dump_only=True)
