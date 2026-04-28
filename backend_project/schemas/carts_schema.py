

from models import Carts
from extensions import ma




class CartsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Carts

    id = ma.auto_field(dump_only=True)
    user_id = ma.auto_field()

    items = ma.Nested('ProductsCartsSchema', many=True)
    status = ma.Function(lambda obj: obj.status.name if obj.status else None)
    total = ma.Method('calculate_total')
    user = ma.Nested('UsersSchema', only=('id', 'username', 'email'))

    def calculate_total(self, obj):
        total = 0

        for item in obj.items:
            total += item.quantity * item.product.price

        return total


from .products_carts_schema import ProductsCartsSchema
from .users_schema import UsersSchema

    




