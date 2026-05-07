
import pytest
from unittest.mock import MagicMock
from services.product_service import ProductService
from models import Products
from repos.products_repo import ProductsRepo
from schemas.products_schema import ProductsSchema
from werkzeug.exceptions import NotFound



def test_product_service_get_function(session):
    #Arrange
    mock_cache = MagicMock()

    mock_cache.get_data.return_value = None

    repo = ProductsRepo(session=session, model=Products, schema=ProductsSchema())

    service = ProductService(cache=mock_cache, repo=repo)

    product1 = Products(id=1, name='Apple', sku='12345', price=5000, brand='apple', stock=1000)
    product2 = Products(id=2, name='Banana', sku='123456', price=3400, brand='sunbum', stock=100)
    session.add_all([product1, product2])
    session.flush()

    filters = {}
    page = 1
    per_page = 20

    #Act
    result = service.get(page, per_page, filters)

    #Assert
    assert len(result['items']) == 2
    assert result['items'][0]['name'] == "Apple"
    assert result['items'][1]['name'] == "Banana"


def test_product_service_get_function_with_filters(session):
    #Arrange
    mock_cache = MagicMock()

    mock_cache.get_data.return_value = None

    repo = ProductsRepo(session=session, model=Products, schema=ProductsSchema())

    service = ProductService(cache=mock_cache, repo=repo)

    product1 = Products(id=1, name='Apple', sku='12345', price=5000, brand='apple', stock=1000)
    product2 = Products(id=2, name='Banana', sku='123456', price=3400, brand='sunbum', stock=100)
    session.add_all([product1, product2])
    session.flush()

    filters = {"name": "Apple"}
    page = 1
    per_page = 20

    #Act
    result = service.get(page, per_page, filters)

    #Assert
    assert len(result['items']) == 1
    assert result['items'][0]['name'] == "Apple"



def test_product_service_get_function_with_id(session):
    #Arrange
    mock_cache = MagicMock()

    mock_cache.get_data.return_value = None

    repo = ProductsRepo(session=session, model=Products, schema=ProductsSchema())

    service = ProductService(cache=mock_cache, repo=repo)

    product1 = Products(id=1, name='Apple', sku='12345', price=5000, brand='apple', stock=1000)
    product2 = Products(id=2, name='Banana', sku='123456', price=3400, brand='sunbum', stock=100)
    session.add_all([product1, product2])
    session.flush()

    id = 1
    page = 1
    per_page = 20

    #Act
    result = service.get(page, per_page, id=id)

    #Assert
    assert result['id'] == 1
    assert result['name'] == "Apple"


def test_product_service_get_function_with_filters_and_id(session):
    #Arrange
    mock_cache = MagicMock()

    mock_cache.get_data.return_value = None

    repo = ProductsRepo(session=session, model=Products, schema=ProductsSchema())

    service = ProductService(cache=mock_cache, repo=repo)

    product1 = Products(id=1, name='Apple', sku='12345', price=5000, brand='apple', stock=1000)
    product2 = Products(id=2, name='Banana', sku='123456', price=3400, brand='sunbum', stock=100)
    session.add_all([product1, product2])
    session.flush()

    id = 2
    filters = {"name": "Apple"}
    page = 1
    per_page = 20

    #Act
    result = service.get(page, per_page, id=id, filters=filters)

    #Assert
    assert result['id'] == 2
    assert result['name'] == "Banana"

def test_product_service_get_function_with_invalid_id(session):
    #Arrange
    mock_cache = MagicMock()

    mock_cache.get_data.return_value = None

    repo = ProductsRepo(session=session, model=Products, schema=ProductsSchema())

    service = ProductService(cache=mock_cache, repo=repo)

    product1 = Products(id=1, name='Apple', sku='12345', price=5000, brand='apple', stock=1000)
    product2 = Products(id=2, name='Banana', sku='123456', price=3400, brand='sunbum', stock=100)
    session.add_all([product1, product2])
    session.flush()

    id = 3
    page = 1
    per_page = 20

    #Act
    with pytest.raises(NotFound):
        service.get(page, per_page, id=id)

    #Assert
    assert NotFound






