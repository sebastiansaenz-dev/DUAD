
from sqlalchemy import select
from models import Carts, ProductsOrders, Products
from constants import CartsStatusEnum, PaymentMethodsEnum
import uuid
from werkzeug.exceptions import BadRequest



from .base_repo import BaseRepository


class OrdersRepo(BaseRepository):
    def __init__(self, model, schema, session=None):
        super().__init__(model, schema, session)


    def proceed_order(self, user_id):
        try:

            cart_stmt = select(Carts).where(Carts.user_id == user_id).where(Carts.status_id == CartsStatusEnum.ACTIVE)

            cart = self.session.execute(cart_stmt).scalars().first()

            products = []

            for item in cart.items:
                p_id = item.product.id
                p_quantity = item.quantity

                product = self.session.get(Products, p_id)

                if p_quantity > product.stock:
                    raise BadRequest(f'not enough stock available for {item.product.name}')
                
                product.stock -= p_quantity

                each_product = {
                    'id': item.product.id,
                    'quantity': item.quantity,
                    'price': item.product.price,
                    'total': item.product.price * item.quantity
                }

                products.append(each_product)


            if not products:
                raise ValueError('your cart is empty, add products to finish your purchase')

            total = 0
            for p in products:
                total += p['total']

            new_order = self.model(
                order_number=uuid.uuid4().hex[:8].upper(),
                user_id=cart.user_id,
                cart_id=cart.id,
                payment_method_id=PaymentMethodsEnum.SINPE,
                total=total
            )

            self.session.add(new_order)
            self.session.flush()

            for p in products:
                new_item = ProductsOrders(
                    order_id=new_order.id,
                    product_id=p['id'],
                    quantity=p['quantity'],
                    price_at_purchase=p['price']
                )
                self.session.add(new_item)
            cart.status_id = CartsStatusEnum.COMPLETED
            self.session.refresh(new_order)
            self.session.commit()

            return new_order


        except Exception as ex:
            self.session.rollback()
            raise ex



