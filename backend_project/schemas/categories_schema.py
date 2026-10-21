from marshmallow import EXCLUDE
from models import Categories
from extensions import ma, db


class CategoriesSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Categories
        load_instance = True
        sqla_session = db.session
        unknown = EXCLUDE

    id = ma.auto_field(dump_only=True)
    name = ma.auto_field(required=True)
