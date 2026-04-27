

from datetime import date as SystemDate
from sqlalchemy import func
from extensions import db


class ProductsCarts(db.Model):
    __tablename__ = 'Products_carts'
    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('Carts.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('Products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    cart = db.relationship('Carts', back_populates='items')
    product = db.relationship('Products')

class ProductsOrders(db.Model):
    __tablename__ = 'Products_orders'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('Orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('Products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price_at_purchase = db.Column(db.Integer, nullable=False)

    order = db.relationship('Orders', back_populates='items')
    product = db.relationship('Products')

class ProductsRefunds(db.Model):
    __tablename__ = 'Products_refunds'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('Products.id'), nullable=False)
    refund_id = db.Column(db.Integer, db.ForeignKey('Refunds.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    total_refunded = db.Column(db.Integer, nullable=False)

    refund = db.relationship('Refunds', back_populates='items')
    product = db.relationship('Products')

class UsersRoles(db.Model):
    __tablename__ = 'Users_roles'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('Roles.id'), server_default='2')

class Users(db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, server_default=func.now())

    refunds = db.relationship('Refunds', back_populates='user')
    carts = db.relationship('Carts', back_populates='user')
    orders = db.relationship('Orders', back_populates='user')
    roles = db.relationship('Roles', secondary=UsersRoles.__table__, back_populates='users', lazy='joined')


class Carts(db.Model):
    __tablename__ = 'Carts'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)
    status_id = db.Column(db.Integer, db.ForeignKey('Carts_status.id'), server_default='1')

    items = db.relationship('ProductsCarts', back_populates='cart', lazy='joined')
    user = db.relationship('Users', back_populates='carts')
    orders = db.relationship('Orders', back_populates='cart')
    status = db.relationship('CartsStatus', back_populates='carts', lazy='joined')

class CartsStatus(db.Model):
    __tablename__ = 'Carts_status'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    carts = db.relationship('Carts', back_populates='status')

class Orders(db.Model):
    __tablename__ = 'Orders'
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(20), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)
    cart_id = db.Column(db.Integer, db.ForeignKey('Carts.id'), nullable=False)
    payment_method_id = db.Column(db.Integer, db.ForeignKey('Payment_methods.id'), nullable=False)
    total = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, server_default=func.now())
    status_id = db.Column(db.Integer, db.ForeignKey('Orders_status.id'), server_default='1')

    user = db.relationship('Users', back_populates='orders')
    payment_method = db.relationship("PaymentMethods", back_populates='orders')
    cart = db.relationship("Carts", back_populates='orders')
    refunds = db.relationship("Refunds", back_populates='order')
    items = db.relationship("ProductsOrders", back_populates='order', lazy='joined')
    status = db.relationship("OrdersStatus")


class OrdersStatus(db.Model):
    __tablename__ = 'Orders_status'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)


class Refunds(db.Model):
    __tablename__ = 'Refunds'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('Orders.id'), nullable=False)
    total = db.Column(db.Integer, nullable=False)
    reason = db.Column(db.String, nullable=False)
    type_id = db.Column(db.Integer, db.ForeignKey('Refunds_types.id'), server_default='1')
    date = db.Column(db.DateTime, server_default=func.now())

    user = db.relationship('Users', back_populates='refunds')
    items = db.relationship('ProductsRefunds', back_populates='refund', lazy='joined')
    order = db.relationship('Orders', back_populates='refunds')
    type = db.relationship('RefundsTypes', back_populates='refund')


class RefundsTypes(db.Model):
    __tablename__ = 'Refunds_types'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    refund = db.relationship('Refunds', back_populates='type')


class PaymentMethods(db.Model):
    __tablename__ = 'Payment_methods'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    orders = db.relationship("Orders", back_populates='payment_method')

class Products(db.Model):
    __tablename__ = 'Products'
    id = db.Column(db.Integer, primary_key=True)
    sku = db.Column(db.String, nullable=False, unique=True)
    name = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    brand = db.Column(db.String, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    entry_date = db.Column(db.DateTime, server_default=func.now())


class Roles(db.Model):
    __tablename__ = 'Roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)

    users = db.relationship('Users', secondary=UsersRoles.__table__, back_populates='roles')

