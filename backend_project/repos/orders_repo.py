from sqlalchemy import select
from models import Carts, ProductsOrders, Products
from constants import CartsStatusEnum, PaymentMethodsEnum
import uuid
from werkzeug.exceptions import BadRequest


from .base_repo import BaseRepository


class OrdersRepo(BaseRepository):
    def __init__(self, model, schema, session=None):
        super().__init__(model, schema, session)

    def _products_from_items(self, items_data):
        products = []

        for item in items_data:
            p_id = int(item.get("id"))
            p_quantity = int(item.get("quantity") or 0)

            if p_quantity < 1:
                raise BadRequest("quantity must be a positive number")

            product = self.session.get(Products, p_id)

            if not product:
                raise BadRequest(f"product {p_id} not found")

            if p_quantity > product.stock:
                raise BadRequest(f"not enough stock available for {product.name}")

            product.stock -= p_quantity

            products.append(
                {
                    "id": product.id,
                    "quantity": p_quantity,
                    "price": product.price,
                    "total": product.price * p_quantity,
                }
            )

        return products

    def _products_from_cart(self, cart):
        products = []

        for item in cart.items:
            p_id = item.product.id
            p_quantity = item.quantity

            product = self.session.get(Products, p_id)

            if p_quantity > product.stock:
                raise BadRequest(f"not enough stock available for {item.product.name}")

            product.stock -= p_quantity

            products.append(
                {
                    "id": item.product.id,
                    "quantity": item.quantity,
                    "price": item.product.price,
                    "total": item.product.price * item.quantity,
                }
            )

        return products

    def proceed_order(self, user_id, order_data):
        try:
            items_data = order_data.get("items") or []
            cart = None

            if user_id:
                cart_stmt = (
                    select(Carts)
                    .where(Carts.user_id == user_id)
                    .where(Carts.status_id == CartsStatusEnum.ACTIVE)
                )
                cart = self.session.execute(cart_stmt).scalars().first()

            if items_data:
                products = self._products_from_items(items_data)
            else:
                if not cart:
                    raise BadRequest(
                        "your cart is empty, add products to finish your purchase"
                    )
                products = self._products_from_cart(cart)

            if not products:
                raise ValueError("your cart is empty, add products to finish your purchase")

            total = sum(p["total"] for p in products)

            new_order = self.model(
                order_number=uuid.uuid4().hex[:8].upper(),
                user_id=int(user_id) if user_id else None,
                cart_id=cart.id if cart else None,
                payment_method_id=PaymentMethodsEnum.SINPE,
                total=total,
                full_name=order_data.get("full_name"),
                address=order_data.get("address"),
                phone=order_data.get("phone"),
            )

            self.session.add(new_order)
            self.session.flush()

            for p in products:
                new_item = ProductsOrders(
                    order_id=new_order.id,
                    product_id=p["id"],
                    quantity=p["quantity"],
                    price_at_purchase=p["price"],
                )
                self.session.add(new_item)

            if cart:
                cart.status_id = CartsStatusEnum.COMPLETED

            self.session.refresh(new_order)
            self.session.commit()

            return new_order

        except Exception as ex:
            self.session.rollback()
            raise ex
