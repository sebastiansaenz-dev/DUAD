


from models import ProductsOrders
from extensions import ma


class ProductsOrdersSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ProductsOrders
        load_instance = True
        exclude = ('id', 'order_id')

    product_id = ma.Function(lambda obj: obj.product.id if obj.product else 'Not found')
    product_name = ma.Function(lambda obj: obj.product.name if obj.product else 'Not found')
    image_url = ma.Function(lambda obj: obj.product.image_url if obj.product else None)
    total = ma.Function(lambda obj: obj.price_at_purchase * obj.quantity if obj.price_at_purchase and obj.quantity else 0)





