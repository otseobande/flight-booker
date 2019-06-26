import json

def test_it_should_validate_request(client):
    response = client.post(
        '/v1/auth/register',
        data=json.dumps({})
    )

    response_body = json.loads(response.data)

    assert response.status_code == 400
    assert response_body == {
        'status': 'error',
        'errors': {
            'password': ['Missing data for required field.'],
            'address': ['Missing data for required field.'],
            'email': ['Missing data for required field.'],
            'full_name': ['Missing data for required field.'],
            'phone_number': ['Missing data for required field.']
        }
    }

def test_it_should_register_user_successfully(client):
    response = client.post(
        '/v1/auth/register',
        data=json.dumps({
            'full_name': 'John Ade',
            'phone_number': '(324) 324 4234',
            'address': '1, afsfad, asdfasf.',
            'email': 'johnade@gmail.com',
            'password': 'password'
        })
    )

    response_body = json.loads(response.data)

    assert response.status_code == 201
    assert response_body['status'] == 'success'
    assert response_body['data']['user']['full_name'] == 'John Ade'
    assert 'password' not in response_body['data']['user']
    assert type(response_body['data']['token']) == str

def test_it_should_return_409_if_email_exists(client):
    client.post(
        '/v1/auth/register',
        data=json.dumps({
            'full_name': 'John Ade',
            'phone_number': '(324) 324 4234',
            'address': '1, afsfad, asdfasf.',
            'email': 'johnade@gmail.com',
            'password': 'password'
        })
    )
    response = client.post(
        '/v1/auth/register',
        data=json.dumps({
            'full_name': 'John Ade',
            'phone_number': '(324) 324 4234',
            'address': '1, afsfad, asdfasf.',
            'email': 'johnade@gmail.com',
            'password': 'password'
        })
    )

    response_body = json.loads(response.data)

    assert response.status_code == 409
    assert response_body['status'] == 'error'
    assert response_body == {
        'status': 'error',
        'message': 'Email is already registered.'
    }
