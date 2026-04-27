


from models import Products
from extensions import ma, db


class ProductsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Products
        load_instance = True
        sqla_session = db.session

        id = ma.auto_field(dump_only=True)



