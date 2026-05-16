


import pytest
from unittest.mock import MagicMock
from services.order_service import OrderService
from models import Orders, Products, Carts, ProductsCarts
from repos.orders_repo import OrdersRepo
from schemas.orders_schema import OrdersSchema
from werkzeug.exceptions import BadRequest


def test_order_service_create_order(session):
    #Arrange

    cache_mock = MagicMock()

    repo = OrdersRepo(session=session, model=Orders, schema=OrdersSchema())

    service = OrderService(cache=cache_mock, repo=repo)

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


    #Act

    result = service.create_order(user_id)


    #Assert
    assert result.id == 1
    assert len(result.items) == 2
    assert result.items[0].product.name == 'Apple'



def test_order_service_create_order_with_no_items(session):
    #Arrange

    cache_mock = MagicMock()


    repo = OrdersRepo(session=session, model=Orders, schema=OrdersSchema())

    service = OrderService(cache=cache_mock, repo=repo)

    user_id = 1

    product1 = Products(id=1, name='Apple', sku='12345', price=5000, brand='apple', stock=1000)
    product2 = Products(id=2, name='Banana', sku='123456', price=3400, brand='sunbum', stock=100)
    session.add_all([product1, product2])
    session.flush()

    
    user_cart = Carts(user_id=user_id)
    session.add(user_cart)
    session.flush()


    #Act
    with pytest.raises(ValueError):
        service.create_order(user_id)


    #Assert
    assert ValueError




def test_order_service_create_order_with_no_items_added_yet(session):
    #Arrange

    cache_mock = MagicMock()

    repo = OrdersRepo(session=session, model=Orders, schema=OrdersSchema())

    service = OrderService(cache=cache_mock, repo=repo)

    user_id = 1

    product1 = Products(id=1, name='Apple', sku='12345', price=5000, brand='apple', stock=1000)
    product2 = Products(id=2, name='Banana', sku='123456', price=3400, brand='sunbum', stock=100)
    session.add_all([product1, product2])
    session.flush()

    #Act
    with pytest.raises(BadRequest):
        service.create_order(user_id)


    #Assert
    assert BadRequest

