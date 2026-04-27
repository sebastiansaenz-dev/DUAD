


from models import ProductsRefunds
from extensions import ma


class ProductsRefundsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ProductsRefunds
        load_instance = True
        include_fk = True

    product_id = ma.auto_field()
    quantity = ma.auto_field()

    product_name = ma.Function(lambda obj: obj.product.name if obj.product else 'Not found')





