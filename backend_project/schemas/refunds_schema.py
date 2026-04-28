

from extensions import ma
from models import Refunds
from marshmallow import fields

class RefundsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Refunds
        include_fk = True

    order_number = fields.String(required=True)

    items = ma.Nested('ProductsRefundsSchema', many=True)

    id = ma.auto_field(dump_only=True)
    total = ma.auto_field(dump_only=True)
    user_id = ma.auto_field()
    order_id = ma.auto_field()

from schemas.products_refunds_schema import ProductsRefundsSchema