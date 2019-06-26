import json

from api.models.user import User

def test_it_return_401_if_authorization_header_is_not_passed(client):
    response = client.post(
        '/v1/flights',
        data=json.dumps({})
    )

    response_body = json.loads(response.data)

    assert response.status_code == 401
    assert response_body == {
        'status': 'error',
        'message': 'Token not provided or is invalid.'
    }

def test_it_should_return_401_if_token_is_invalid(client):
    response = client.post(
        '/v1/flights',
        data=json.dumps({}),
        headers={
            'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c'
        }
    )

    response_body = json.loads(response.data)

    assert response.status_code == 401
    assert response_body == {
        'status': 'error',
        'message': 'Token not provided or is invalid.'
    }

def test_it_should_return_401_if_bearer_is_not_included(client):
    response = client.post(
        '/v1/flights',
        data=json.dumps({}),
        headers={
            'Authorization': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c'
        }
    )

    response_body = json.loads(response.data)

    assert response.status_code == 401
    assert response_body == {
        'status': 'error',
        'message': 'Token not provided or is invalid.'
    }

def test_it_should_validate_user_input(client):
    user = User(
        full_name='John Ade',
        phone_number='(324) 324 4234',
        address='1, afsfad, asdfasf.',
        email='johnade@gmail.com',
        password='password'
    )
    user.save()

    token = user.generate_token()

    response = client.post(
        '/v1/flights',
        data=json.dumps({}),
        headers={
            'Authorization': 'Bearer ' + token
        }
    )

    response_body = json.loads(response.data)

    assert response.status_code == 400
    assert response_body == {
        'status': 'error',
        'errors': {
            'estimated_arrival_time': ['Missing data for required field.'],
            'airline': ['Missing data for required field.'],
            'departure_time': ['Missing data for required field.'],
            'fare': ['Missing data for required field.'],
            'max_capacity': ['Missing data for required field.'],
            'destination': ['Missing data for required field.'],
            'origin': ['Missing data for required field.']
        }
    }

def test_it_should_create_a_flight_successfully(client):
    user = User(
        full_name='John Ade',
        phone_number='(324) 324 4234',
        address='1, afsfad, asdfasf.',
        email='johnade@gmail.com',
        password='password'
    )
    user.save()

    token = user.generate_token()

    response = client.post(
        '/v1/flights',
        data=json.dumps({
            'estimated_arrival_time': '2014-12-22T03:12:58.019077+00:00',
            'airline': 'Arik',
            'departure_time': '2014-12-22T03:12:58.019077+00:00',
            'fare': 50000,
            'max_capacity': 40,
            'destination': 'Enugu',
            'origin': 'Calabar'
        }),
        headers={
            'Authorization': 'Bearer ' + token
        }
    )

    response_body = json.loads(response.data)

    assert response.status_code == 201
    assert response_body['status'] == 'success'
    assert response_body['data']['flight']['airline'] == 'Arik'

