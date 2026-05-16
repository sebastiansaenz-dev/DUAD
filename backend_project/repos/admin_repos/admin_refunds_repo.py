
from repos.base_repo import BaseRepository
from sqlalchemy import select
from models import Orders, ProductsRefunds, Products
from constants import OrdersStatusEnum
from werkzeug.exceptions import NotFound, BadRequest



class AdminRefundsRepo(BaseRepository):
    def __init__(self, model, schema, session=None):
        super().__init__(model, schema, session)


    def refund_status(self, original_items, validate_items, history):

        total_purchase = sum(item['quantity'] for item in original_items.values())

        total_past_refunded = sum(history.values())

        total_current_refunded = sum(item['quantity'] for item in validate_items)

        if (total_past_refunded + total_current_refunded) >= total_purchase:
            return 'FULL'
        
        else:
            return 'PARTIAL'


    def create_refund(self, current_user_id, data):
        try:
            self.schema.load(data, partial=True)
            print(data['order_number'])
            order_stmt = select(Orders).where(Orders.user_id == current_user_id).where(Orders.order_number == data['order_number']).where(Orders.status_id == OrdersStatusEnum.COMPLETED)
            

            order = self.session.execute(order_stmt).scalars().unique().first()

            items_to_refund = data['items']
            print(data['items'])

            if not order:
                raise NotFound('order not found')

            self.session.refresh(order)

            original_items = {
                p.product.id: {
                    'quantity': p.quantity,
                    'price': p.price_at_purchase
                } for p in order.items
            }

            print(f'orders: {order.refunds}')

            history = {}
            for r in list(order.refunds):
                for ri in r.items:
                    history[ri.product_id] = history.get(ri.product_id, 0) + ri.quantity

            total_to_refund = 0
            validate_items = []


            for item in items_to_refund:
                p_id = item['product_id']
                p_quantity = item['quantity']

                if not p_id in original_items:
                    raise BadRequest(f'product_id {p_id} was not part of this order')
                
                original_quantity = original_items[p_id]['quantity']

                already_refunded = history.get(p_id, 0)

                if (p_quantity + already_refunded) > original_quantity:
                    raise BadRequest(f'the quantity for product_id: {p_id} exceeds the quantity bought')

                if p_quantity <= 0:
                    raise BadRequest(f'invalid quantity for product {p_id}')

                price = original_items[p_id]['price']
                subtotal = price * p_quantity
                total_to_refund += subtotal

                validate_items.append({
                    'product_id': p_id,
                    'quantity': p_quantity,
                    'total_refund': subtotal
                })

            print(validate_items)

            new_refund = self.model(
                user_id=current_user_id,
                order_id=order.id,
                total=total_to_refund,
                reason=data['reason']
            )

            self.session.add(new_refund)
            self.session.flush()

            for item in validate_items:
                new_item = ProductsRefunds(
                    product_id=item['product_id'],
                    refund_id=new_refund.id,
                    quantity=item['quantity'],
                    total_refunded=item['total_refund']
                )
                self.session.add(new_item)

                product = self.session.get(Products, item['product_id'])
                product.stock += item['quantity']
            
            status = self.refund_status(original_items, validate_items, history)

            if status == 'FULL':
                order.status_id = OrdersStatusEnum.REFUNDED

            elif status == 'PARTIAL':
                order.status_id = OrdersStatusEnum.PARTIALLY_REFUNDED

            self.session.commit()

            return self.schema.dump(new_refund)


        except Exception as ex:
            self.session.rollback()
            print(ex)
            raise ex

