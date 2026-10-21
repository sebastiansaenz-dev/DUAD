import uuid
from flask_jwt_extended import create_access_token


def _headers(client, role):
    additional_claims = {"roles": [role]}
    with client.application.app_context():
        token = create_access_token(identity='1', additional_claims=additional_claims)
    return {'Authorization': f'Bearer {token}'}


def _admin_headers(client):
    return _headers(client, 'admin')


def _client_headers(client):
    return _headers(client, 'client')


def _unique_name(prefix):
    return f'{prefix}-{uuid.uuid4().hex[:8]}'


def _create_category(client, name=None):
    payload = {'name': name or _unique_name('Category')}
    response = client.post('/staff-portal/categories/', headers=_admin_headers(client), json=payload)
    assert response.status_code == 201
    body = response.get_json()
    assert 'error' not in body
    return body


def test_admin_can_create_read_update_delete_category(client):
    admin = _admin_headers(client)
    name = _unique_name('Home')

    create_response = client.post('/staff-portal/categories/', headers=admin, json={'name': name})
    assert create_response.status_code == 201
    created = create_response.get_json()
    assert created['name'] == name
    assert created['id'] is not None
    category_id = created['id']

    list_response = client.get('/staff-portal/categories/', headers=admin)
    assert list_response.status_code == 200
    assert any(item['id'] == category_id for item in list_response.get_json())

    get_response = client.get(f'/staff-portal/categories/{category_id}', headers=admin)
    assert get_response.status_code == 200
    assert get_response.get_json()['name'] == name

    updated_name = _unique_name('Kitchen')
    patch_response = client.patch(
        f'/staff-portal/categories/{category_id}',
        headers=admin,
        json={'name': updated_name},
    )
    assert patch_response.status_code == 200
    assert patch_response.get_json()['name'] == updated_name

    delete_response = client.delete(f'/staff-portal/categories/{category_id}', headers=admin)
    assert delete_response.status_code == 200
    assert delete_response.get_json()['message'] == 'item deleted'

    missing_response = client.get(f'/staff-portal/categories/{category_id}', headers=admin)
    assert missing_response.status_code == 404


def test_admin_cannot_create_duplicate_or_empty_category(client):
    admin = _admin_headers(client)
    name = _unique_name('Sports')
    first = client.post('/staff-portal/categories/', headers=admin, json={'name': name})
    assert first.status_code == 201

    duplicate = client.post('/staff-portal/categories/', headers=admin, json={'name': name})
    assert duplicate.status_code == 409

    empty = client.post('/staff-portal/categories/', headers=admin, json={'name': '   '})
    assert empty.status_code == 400


def test_admin_update_and_delete_missing_category(client):
    admin = _admin_headers(client)

    patch_response = client.patch('/staff-portal/categories/999999', headers=admin, json={'name': 'Missing'})
    assert patch_response.status_code == 404

    delete_response = client.delete('/staff-portal/categories/999999', headers=admin)
    assert delete_response.status_code == 404


def test_admin_cannot_delete_category_with_products(client):
    admin = _admin_headers(client)
    category = _create_category(client)

    product_response = client.post(
        '/staff-portal/products/',
        headers=admin,
        json={
            'name': _unique_name('Product'),
            'price': 1500,
            'stock': 10,
            'category': category['name'],
        },
    )
    assert product_response.status_code == 200
    product = product_response.get_json()
    assert product['category'] == category['name']

    delete_response = client.delete(f'/staff-portal/categories/{category["id"]}', headers=admin)
    assert delete_response.status_code == 400

    product_delete = client.delete(f'/staff-portal/products/{product["id"]}', headers=admin)
    assert product_delete.status_code == 200, product_delete.get_json()

    category_delete = client.delete(f'/staff-portal/categories/{category["id"]}', headers=admin)
    assert category_delete.status_code == 200


def test_renaming_category_does_not_break_products(client):
    admin = _admin_headers(client)
    category = _create_category(client, _unique_name('Gadgets'))

    product_response = client.post(
        '/staff-portal/products/',
        headers=admin,
        json={
            'name': _unique_name('Phone'),
            'price': 2000,
            'stock': 4,
            'category': category['name'],
        },
    )
    assert product_response.status_code == 200
    product_id = product_response.get_json()['id']

    new_name = _unique_name('Electronics')
    patch_response = client.patch(
        f'/staff-portal/categories/{category["id"]}',
        headers=admin,
        json={'name': new_name},
    )
    assert patch_response.status_code == 200

    product = client.get(f'/products/{product_id}').get_json()
    assert product['category'] == new_name
    assert 'error' not in product


def test_client_can_view_categories_but_cannot_mutate(client):
    admin = _admin_headers(client)
    client_headers = _client_headers(client)
    category = _create_category(client, _unique_name('Office'))

    list_response = client.get('/categories/', headers=client_headers)
    assert list_response.status_code == 200
    assert any(item['id'] == category['id'] for item in list_response.get_json())

    get_response = client.get(f'/categories/{category["id"]}', headers=client_headers)
    assert get_response.status_code == 200
    assert get_response.get_json()['name'] == category['name']

    create_response = client.post(
        '/staff-portal/categories/',
        headers=client_headers,
        json={'name': _unique_name('Forbidden')},
    )
    assert create_response.status_code == 403

    patch_response = client.patch(
        f'/staff-portal/categories/{category["id"]}',
        headers=client_headers,
        json={'name': 'Hacked'},
    )
    assert patch_response.status_code == 403

    delete_response = client.delete(
        f'/staff-portal/categories/{category["id"]}',
        headers=client_headers,
    )
    assert delete_response.status_code == 403

    still_there = client.get(f'/categories/{category["id"]}', headers=client_headers)
    assert still_there.status_code == 200
    assert still_there.get_json()['name'] == category['name']

    client_write = client.post('/categories/', headers=client_headers, json={'name': 'Nope'})
    assert client_write.status_code == 405

    cleanup = client.delete(f'/staff-portal/categories/{category["id"]}', headers=admin)
    assert cleanup.status_code == 200


def test_unauthenticated_user_cannot_read_or_mutate_categories(client):
    category = _create_category(client)

    assert client.get('/categories/').status_code == 401
    assert client.get(f'/categories/{category["id"]}').status_code == 401
    assert client.post('/staff-portal/categories/', json={'name': 'Nope'}).status_code == 401
    assert client.patch(
        f'/staff-portal/categories/{category["id"]}',
        json={'name': 'Nope'},
    ).status_code == 401
    assert client.delete(f'/staff-portal/categories/{category["id"]}').status_code == 401
