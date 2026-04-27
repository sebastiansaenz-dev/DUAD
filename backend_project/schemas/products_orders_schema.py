


from models import ProductsOrders
from extensions import ma


class ProductsOrdersSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ProductsOrders
        load_instance = True
        exclude = ('id', 'order_id', 'product_id')

    product_name = ma.Function(lambda obj: obj.product.name if obj.product else 'Not found')





