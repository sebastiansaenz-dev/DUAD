

import pytest
from services.refund_service import RefundService
from models import Refunds, ProductsRefunds
from repos.refunds_repo import RefundsRepo
from schemas.refunds_schema import RefundsSchema
from werkzeug.exceptions import BadRequest
from constants import OrdersStatusEnum



def test_refund_service_get_refunds_function(session, setup_order):

    repo = RefundsRepo(session=session, model=Refunds, schema=RefundsSchema())

    service = RefundService(repo=repo)


    old_refund = Refunds(user_id=setup_order['user_id'], order_id=setup_order['order'].id, total=setup_order['order'].total, reason='bad item')
    session.add(old_refund)
    session.flush()

    product_refund1 = ProductsRefunds(
        product_id=setup_order['products'][0].id,
        refund_id=old_refund.id,
        quantity=setup_order['products_orders'][0].quantity,
        total_refunded=int(setup_order['products_orders'][0].quantity * setup_order['products'][0].price)
    )

    session.add(product_refund1)
    session.flush()



    #Act
    result = service.get_refunds(setup_order['user_id'])



    #Assert
    assert result[0]['id'] == 1
    assert len(result[0]['items']) == 1


def test_service_crate_refund(session, setup_order):
    repo = RefundsRepo(session=session, model=Refunds, schema=RefundsSchema())

    service = RefundService(repo=repo)


    data = {
        "order_number": '123',
        "reason": "Bad item",
        "items": [
            {
                "product_id": 1,
                "quantity": 2
            }
        ]
    }

    #Act
    result = service.create_refund(user_id=setup_order['user_id'], data=data)

    #Assert
    assert result.id == 1
    assert len(result.items) == 1
    assert result.items[0].product.stock == 1002



def test_service_crate_refund_partially_refunded(session, setup_order):
    repo = RefundsRepo(session=session, model=Refunds, schema=RefundsSchema())

    service = RefundService(repo=repo)


    data = {
        "order_number": '123',
        "reason": "Bad item",
        "items": [
            {
                "product_id": 1,
                "quantity": 2
            }
        ]
    }

    #Act
    result = service.create_refund(user_id=setup_order['user_id'], data=data)

    #Assert
    assert result.id == 1
    assert len(result.items) == 1
    assert result.items[0].product.stock == 1002
    assert setup_order['order'].status_id == OrdersStatusEnum.PARTIALLY_REFUNDED


def test_service_crate_refund_totally_refunded(session, setup_order):
    repo = RefundsRepo(session=session, model=Refunds, schema=RefundsSchema())

    service = RefundService(repo=repo)


    data = {
        "order_number": '123',
        "reason": "Bad item",
        "items": [
            {
                "product_id": 1,
                "quantity": 4
            },
            {
                "product_id": 2,
                "quantity": 6
            }
        ]
    }

    #Act
    result = service.create_refund(user_id=setup_order['user_id'], data=data)

    #Assert
    assert result.id == 1
    assert len(result.items) == 2
    assert result.items[0].product.stock == 1004
    assert result.items[1].product.stock == 106
    assert setup_order['order'].status_id == OrdersStatusEnum.REFUNDED



def test_service_crate_refund_with_diferent_product_id(session, setup_order):
    repo = RefundsRepo(session=session, model=Refunds, schema=RefundsSchema())

    service = RefundService(repo=repo)


    data = {
        "order_number": '123',
        "reason": "Bad item",
        "items": [
            {
                "product_id": 3,
                "quantity": 4
            },
            {
                "product_id": 4,
                "quantity": 6
            }
        ]
    }

    #Act
    with pytest.raises(BadRequest):
        service.create_refund(user_id=setup_order['user_id'], data=data)

    #Assert
    assert BadRequest


def test_service_crate_refund_with_more_quantity(session, setup_order):
    repo = RefundsRepo(session=session, model=Refunds, schema=RefundsSchema())

    service = RefundService(repo=repo)


    data = {
        "order_number": '123',
        "reason": "Bad item",
        "items": [
            {
                "product_id": 1,
                "quantity": 40
            }
        ]
    }

    #Act
    with pytest.raises(BadRequest):
        service.create_refund(user_id=setup_order['user_id'], data=data)

    #Assert
    assert BadRequest
