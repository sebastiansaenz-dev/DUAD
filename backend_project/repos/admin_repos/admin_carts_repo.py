



from repos.base_repo import BaseRepository
from models import ProductsCarts, Products
from sqlalchemy import select
from extensions import db
from werkzeug.exceptions import NotFound, BadRequest, Conflict
from constants import CartsStatusEnum


class AdminCartsRepo(BaseRepository):
    def add_products(self, user_id, products):
        try:
            cart_stmt = select(self.model).where(self.model.user_id == user_id).where(self.model.status_id == CartsStatusEnum.ACTIVE)

            cart = db.session.execute(cart_stmt).scalars().first()

            if not cart:
                cart = self.model(user_id=user_id)
                db.session.add(cart)
                db.session.flush()

            for p in products:
                p_id = int(p['id'])
                p_quantity = int(p['quantity'])

                if p_quantity < 0:
                    raise BadRequest('quantity must be a positive number')

                product = db.session.get(Products, p_id)

                if not product:
                    raise NotFound('product not found')


                item_stmt = select(ProductsCarts).where(ProductsCarts.cart_id == cart.id).where(ProductsCarts.product_id == p_id)
                item = db.session.execute(item_stmt).scalars().first()

                if p_quantity > product.stock:
                    raise BadRequest('not enough stock available')
                
                if item:
                    item.quantity += p_quantity
                
                else:
                    new_item = ProductsCarts(
                        cart_id=cart.id,
                        product_id=p_id,
                        quantity=p_quantity
                    )
                    db.session.add(new_item)                
                product.stock -= p_quantity
            db.session.commit()
        except Exception as ex:
            db.session.rollback()
            raise ex

    
    def update_quantity(self, user_id, products):
        try:
            cart_stmt = select(self.model).where(self.model.user_id == user_id).where(self.model.status_id == CartsStatusEnum.ACTIVE)

            cart = db.session.execute(cart_stmt).scalars().first()

            for p in products:

                product_id = p['id']
                new_quantity = p['quantity']

                item_stmt = select(ProductsCarts).where(ProductsCarts.cart_id == cart.id).where(ProductsCarts.product_id == product_id)
                item = db.session.execute(item_stmt).scalars().first()

                if not item:
                    raise NotFound('product not found')
                
                product = db.session.get(Products, product_id)
                
                if new_quantity == 0:
                    product.stock += item.quantity
                    db.session.delete(item)
                
                difference = new_quantity - item.quantity

                if difference > product.stock:
                    raise Conflict('not enough stock available')
                
                product.stock -= difference
                item.quantity = new_quantity

                db.session.commit()


        except Exception as ex:
            db.session.rollback()
            raise ex
    

    def delete_product(self, user_id, products):
        try:
            cart_stmt = select(self.model).where(self.model.user_id == user_id).where(self.model.status_id == CartsStatusEnum.ACTIVE)

            cart = db.session.execute(cart_stmt).scalars().first()

            for p in products:
                product_id = p['id']

                item_stmt = select(ProductsCarts).where(ProductsCarts.cart_id == cart.id).where(ProductsCarts.product_id == product_id)

                item = db.session.execute(item_stmt).scalars().first()

                if not item:
                    raise NotFound('product not found')
                
                product = db.session.get(Products, product_id)

                product.stock += item.quantity

                db.session.delete(item)

            db.session.commit()

        except Exception as ex:
            db.session.rollback()
            raise ex






