import json, io

from api.models.user import User
from api.models.flight import Flight
from api.models.flight_ticket import FlightTicket

def test_it_return_401_if_authorization_header_is_not_passed(client):
    response = client.post(
        '/v1/user/upload-passport',
        data=json.dumps({})
    )

    response_body = json.loads(response.data)

    assert response.status_code == 401
    assert response_body == {
        'status': 'error',
        'message': 'Token not provided or is invalid.'
    }

def test_it_should_validate_input(client):
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
        '/v1/user/upload-passport',
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
            'image': ['Missing data for required field.']
        }
    }

def test_uploaded_file_should_be_the_right_format(client):
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
        '/v1/user/upload-passport',
        data={
            'image': (io.BytesIO(b'Test data'), 'file.pdf')
        },
        headers={
            'Authorization': 'Bearer ' + token
        }
    )

    response_body = json.loads(response.data)

    assert response.status_code == 400
    assert response_body == {
        'status': 'error',
        'errors': {
            'image': ['Only .jpg and .png file extensions are allowed.']
        }
    }

def test_it_should_upload_passport_photo_successfully(client):
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
        '/v1/user/upload-passport',
        data={
            'image': (io.BytesIO(b'Test data'), 'image.png')
        },
        headers={
            'Authorization': 'Bearer ' + token
        }
    )

    response_body = json.loads(response.data)

    assert response.status_code == 200
    assert response_body['status'] == 'success'
    assert response_body['message'] == 'Passport photo uploaded successfully'
    assert response_body['data']['user']['id'] == str(user.id)
    assert 'image.png' in response_body['data']['user']['passport_photo_url']
