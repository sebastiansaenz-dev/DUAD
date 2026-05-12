import pytest
from flask_jwt_extended import create_access_token



def test_require_auth_with_valid_token(client):

    additional_claims = {"roles": ["client"]}


    with client.application.app_context():
        valid_token = create_access_token(identity="1", additional_claims=additional_claims)

    headers = {'Authorization': f'Bearer {valid_token}'}
    response = client.get('/cart/', headers=headers)

    assert response.status_code == 200


def test_require_auth_admin_token(client):
    additional_claims = {"roles": ["admin"]}

    with client.application.app_context():
        admin_token = create_access_token(identity='1', additional_claims=additional_claims)

    headers = {'Authorization': f'Bearer {admin_token}'}

    payload = {
        "name": "apple",
        "price": 123,
        'stock': 44,
        'brand': 'apples_brand'
    }

    response = client.post('/staff-portal/products/', headers=headers, json=payload)

    assert response.status_code == 200


def test_require_auth_only_admin_with_client_token(client):

    additional_claims = {"roles": ["client"]}

    with client.application.app_context():
        client_token = create_access_token(identity='1', additional_claims=additional_claims)

    headers = {'Authorization': f'Bearer {client_token}'}


    response = client.post('/staff-portal/products/', headers=headers)

    assert response.status_code == 403


def test_require_auth_admin_only_with_no_token(client):

    response = client.post('/staff-portal/products/')

    assert response.status_code == 401


def test_require_aut_with_no_token(client):

    response = client.post('/cart/')

    assert response.status_code == 401
