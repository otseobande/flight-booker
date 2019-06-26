import json

from api.models.user import User

def test_it_should_validate_request(client):
    response = client.post(
        '/v1/auth/login',
        data=json.dumps({})
    )

    response_body = json.loads(response.data)

    assert response.status_code == 400
    assert response_body == {
        'status': 'error',
        'errors': {
            'password': ['Missing data for required field.'],
            'email': ['Missing data for required field.'],
        }
    }

def test_it_should_return_401_if_email_is_not_registered(client):
    response = client.post(
        '/v1/auth/login',
        data=json.dumps({
            'email': 'j@gmail.com',
            'password': 'password'
        })
    )

    response_body = json.loads(response.data)

    assert response.status_code == 401
    assert response_body == {
        'status': 'error',
        'message': 'Email or password is incorrect, please check your credentials.'
    }

def test_it_should_return_401_if_password_is_incorrect(client):
    user = User(
        full_name='John Ade',
        phone_number='(324) 324 4234',
        address='1, afsfad, asdfasf.',
        email='johnade@gmail.com',
        password='password'
    )
    user.save()

    response = client.post(
        '/v1/auth/login',
        data=json.dumps({
            'email': user.email,
            'password': 'wrongpassword'
        })
    )

    response_body = json.loads(response.data)

    assert response.status_code == 401
    assert response_body == {
        'status': 'error',
        'message': 'Email or password is incorrect, please check your credentials.'
    }

def test_it_should_login_a_user_successfully(client):
    user = User(
        full_name='John Ade',
        phone_number='(324) 324 4234',
        address='1, afsfad, asdfasf.',
        email='johnade@gmail.com',
        password='password'
    )
    user.save()

    response = client.post(
        '/v1/auth/login',
        data=json.dumps({
            'email': user.email,
            'password': 'password'
        })
    )

    response_body = json.loads(response.data)

    assert response.status_code == 200
    assert response_body['status'] == 'success'
    assert response_body['data']['user']['full_name'] == 'John Ade'
    assert 'password' not in response_body['data']['user']
    assert type(response_body['data']['token']) == str
