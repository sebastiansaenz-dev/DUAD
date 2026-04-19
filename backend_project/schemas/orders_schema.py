

from models import Orders
from extensions import ma



class OrdersSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Orders
        load_instance = True

    id = ma.auto_field(dump_only=True)
    user_id = ma.auto_field(load_only=True)


    user = ma.Nested('UsersSchema', only=('id', 'username'))
    payment_method_name = ma.Function(lambda obj: obj.payment_method.name if obj.payment_method else None)
    status = ma.Function(lambda obj: obj.status.name if obj.status else None)
    items = ma.Nested('ProductsOrdersSchema', many=True)
    

from .users_schema import UsersSchema
from .products_orders_schema import ProductsOrdersSchema




