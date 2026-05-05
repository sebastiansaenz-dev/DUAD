
from sqlalchemy import select
from models import Carts, ProductsOrders, OrdersStatus, Orders
from constants import CartsStatusEnum, PaymentMethodsEnum
import uuid
from werkzeug.exceptions import BadRequest, NotFound



from repos.base_repo import BaseRepository


class AdminOrdersRepo(BaseRepository):
    def __init__(self, model, schema, session=None):
        super().__init__(model, schema, session)


    def create_order(self, user_id):
        try:
            cart_stmt = select(Carts).where(Carts.user_id == user_id).where(Carts.status_id == CartsStatusEnum.ACTIVE)

            cart = self.session.execute(cart_stmt).scalars().first()

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
            self.session.commit()

            return self.schema.dump(new_order)


        except Exception as ex:
            self.session.rollback()
            raise ex
        
    def update_status(self, user_id, data):

        if 'status' not in data:
            raise BadRequest('missing field: status')

        order_stmt = select(Orders).where(Orders.user_id == user_id)

        order = self.session.execute(order_stmt).scalars().unique().first()

        if not order:
            raise NotFound('order not found')

        new_status_stmt = select(OrdersStatus).where(OrdersStatus.name == data['status'])
        new_status = self.session.execute(new_status_stmt).scalars().first()

        if not new_status:
            raise BadRequest(f'invalid status: {data['status']}')
                
        order.status_id = new_status.id

        self.session.commit()
        self.session.refresh(order)

        return self.schema.dump(order)







