


import pytest
from unittest.mock import MagicMock
from services.order_service import OrderService



def test_order_service_create_order():
    #Arrange
    mock_cache = MagicMock()
    mock_repo = MagicMock()
    user_id = 1


    mock_cache.get_data.return_value = None

    item1 = MagicMock()
    item1.product_id = 101
    item1.product.stock = 7

    item2 = MagicMock()
    item2.product_id = 102
    item2.product.stock = 3


    mock_order = MagicMock()
    mock_order.items = [item1, item2]

    mock_repo.proceed_order.return_value = mock_order
    

    service = OrderService(cache=mock_cache, repo=mock_repo)

    #Act

    result = service.create_order(user_id)


    #Assert
    assert result == mock_order
    mock_repo.proceed_order.assert_called_once_with(user_id)






