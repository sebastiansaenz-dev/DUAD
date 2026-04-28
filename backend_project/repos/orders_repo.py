
from extensions import db
from sqlalchemy import select
from models import Carts, ProductsOrders
from constants import CartsStatusEnum, PaymentMethodsEnum
import uuid



from .base_repo import BaseRepository


class OrdersRepo(BaseRepository):
    def create_order(self, user_id):
        try:
            cart_stmt = select(Carts).where(Carts.user_id == user_id).where(Carts.status_id == CartsStatusEnum.ACTIVE)

            cart = db.session.execute(cart_stmt).scalars().first()

            products = [{
                'id': p.product.id,
                'quantity': p.quantity,
                'price': p.product.price,
                'total': p.product.price * p.quantity
            } for p in cart.items]

            if not products:
                raise ValueError('your cart is empty, add products to finish your purchase')

            total = 0
            for p in products:
                total += p['total']

            new_order = self.model(
                order_number=uuid.uuid4().hex[:8].upper(),
                user_id=user_id,
                cart_id=cart.id,
                payment_method_id=PaymentMethodsEnum.SINPE,
                total=total
            )

            db.session.add(new_order)
            db.session.flush()

            for p in products:
                new_item = ProductsOrders(
                    order_id=new_order.id,
                    product_id=p['id'],
                    quantity=p['quantity'],
                    price_at_purchase=p['price']
                )

                db.session.add(new_item)
            cart.status_id = CartsStatusEnum.COMPLETED
            db.session.commit()

            return self.schema.dump(new_order)


        except Exception as ex:
            db.session.rollback()
            raise ex



