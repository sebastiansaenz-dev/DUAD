import pytest
from flask_jwt_extended import create_access_token
from models import Categories, Products
from repos.categories_repo import CategoriesRepo
from schemas.categories_schema import CategoriesSchema
from services.admin_services.admin_category_service import AdminCategoryService
from werkzeug.exceptions import BadRequest, Conflict, NotFound


def _admin_headers(client):
    additional_claims = {"roles": ["admin"]}
    with client.application.app_context():
        admin_token = create_access_token(identity='1', additional_claims=additional_claims)
    return {'Authorization': f'Bearer {admin_token}'}


def _client_headers(client):
    additional_claims = {"roles": ["client"]}
    with client.application.app_context():
        client_token = create_access_token(identity='1', additional_claims=additional_claims)
    return {'Authorization': f'Bearer {client_token}'}


def test_create_category(session):
    repo = CategoriesRepo(session=session, model=Categories, schema=CategoriesSchema())
    service = AdminCategoryService(repo=repo)

    result = service.create_category({'name': ' Electronics-test '})

    assert result['name'] == 'Electronics-test'
    assert result['id'] is not None


def test_create_category_duplicate_name(session):
    repo = CategoriesRepo(session=session, model=Categories, schema=CategoriesSchema())
    service = AdminCategoryService(repo=repo)
    service.create_category({'name': 'Electronics-dup'})

    with pytest.raises(Conflict):
        service.create_category({'name': 'Electronics-dup'})


def test_update_category(session):
    repo = CategoriesRepo(session=session, model=Categories, schema=CategoriesSchema())
    service = AdminCategoryService(repo=repo)
    created = service.create_category({'name': 'Home'})

    result = service.update_category(created['id'], {'name': 'Kitchen'})

    assert result['name'] == 'Kitchen'


def test_delete_category(session):
    repo = CategoriesRepo(session=session, model=Categories, schema=CategoriesSchema())
    service = AdminCategoryService(repo=repo)
    created = service.create_category({'name': 'Sports'})

    deleted = service.delete_category(created['id'])

    assert deleted is True
    with pytest.raises(NotFound):
        service.get_by_id(created['id'])


def test_delete_category_with_products(session):
    repo = CategoriesRepo(session=session, model=Categories, schema=CategoriesSchema())
    service = AdminCategoryService(repo=repo)
    category = Categories(name='Pets')
    session.add(category)
    session.flush()
    session.add(Products(name='Collar', sku='CAT0000001', price=1000, category_id=category.id, stock=5))
    session.flush()

    with pytest.raises(BadRequest):
        service.delete_category(category.id)


def test_admin_categories_crud_endpoint(client):
    headers = _admin_headers(client)

    create_response = client.post('/staff-portal/categories/', headers=headers, json={'name': 'Office'})
    assert create_response.status_code == 201
    category_id = create_response.get_json()['id']

    list_response = client.get('/staff-portal/categories/', headers=headers)
    assert list_response.status_code == 200
    assert any(item['id'] == category_id for item in list_response.get_json())

    get_response = client.get(f'/staff-portal/categories/{category_id}', headers=headers)
    assert get_response.status_code == 200
    assert get_response.get_json()['name'] == 'Office'

    patch_response = client.patch(
        f'/staff-portal/categories/{category_id}',
        headers=headers,
        json={'name': 'Office Supplies'}
    )
    assert patch_response.status_code == 200
    assert patch_response.get_json()['name'] == 'Office Supplies'

    delete_response = client.delete(f'/staff-portal/categories/{category_id}', headers=headers)
    assert delete_response.status_code == 200


def test_admin_categories_staff_portal_is_forbidden_for_client_mutations(client):
    headers = _client_headers(client)
    response = client.post('/staff-portal/categories/', headers=headers, json={'name': 'Office'})
    assert response.status_code == 403
