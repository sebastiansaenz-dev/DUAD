


from models import ProductsCarts
from extensions import ma


class ProductsCartsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ProductsCarts
        load_instance = True
        include_fk = True

    product_id = ma.auto_field()
    quantity = ma.auto_field()

    product_name = ma.Function(lambda obj: obj.product.name if obj.product else 'Not found')
    price = ma.Function(lambda obj: obj.product.price if obj.product else None)





