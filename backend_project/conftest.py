
import pytest
from extensions import db as _db
from app import create_app
from sqlalchemy.orm import sessionmaker

from models import Products, ProductsOrders, ProductsCarts, Carts, Orders
from constants import OrdersStatusEnum, PaymentMethodsEnum

@pytest.fixture(scope='session')
def app():
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'REDIS_HOST': None
    })

    return app


@pytest.fixture(scope='session')
def db(app):
    with app.app_context():

        if _db.engine.url.drivername == 'sqlite':
            for table in _db.metadata.tables.values():
                table.schema = None

        _db.create_all()
        yield _db
        _db.drop_all()


@pytest.fixture()
def session(db, app):
    with app.app_context():
        connection = db.engine.connect()
        transaction = connection.begin()

        Session = sessionmaker(bind=connection)
        session = Session()


        yield session

        session.close()
        if transaction.is_active:
            transaction.rollback()
        connection.close()


@pytest.fixture()
def setup_order(session):
    user_id = 1


    product1 = Products(id=1, name='Apple', sku='12345', price=5000, brand='apple', stock=1000)

    product2 = Products(id=2, name='Banana', sku='123456', price=3400, brand='sunbum', stock=100)

    session.add_all([product1, product2])
    session.flush()

    user_cart = Carts(user_id=user_id)
    session.add(user_cart)
    session.flush()

    product_cart1 = ProductsCarts(cart_id=user_cart.id, product_id=product1.id, quantity=4)

    product_cart2 = ProductsCarts(cart_id=user_cart.id, product_id=product2.id, quantity=6)

    session.add_all([product_cart1, product_cart2])
    session.flush()

    total = (product1.price * product_cart1.quantity) + (product2.price * product_cart2.quantity)

    order = Orders(order_number='123', user_id=user_id, cart_id=user_cart.id, payment_method_id=PaymentMethodsEnum.SINPE, total=total, status_id=OrdersStatusEnum.COMPLETED)

    session.add(order)
    session.flush()

    product_order1 = ProductsOrders(order_id=order.id, product_id=product1.id, quantity=product_cart1.quantity, price_at_purchase=product1.price)

    product_order2 = ProductsOrders(order_id=order.id, product_id=product2.id, quantity=product_cart2.quantity, price_at_purchase=product2.price)

    session.add_all([product_order1, product_order2])
    session.flush()

    session.refresh(order)

    return {
        "order": order,
        "user_id": user_id,
        "products": [
            product1, product2
        ],
        "products_orders": [
            product_order1, product_order2
        ]
    }
















