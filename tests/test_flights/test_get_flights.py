import json
from api.models.user import User
from api.models.flight import Flight

def test_it_return_401_if_authorization_header_is_not_passed(client):
    response = client.get('/v1/flights')

    response_body = json.loads(response.data)

    assert response.status_code == 401
    assert response_body == {
        'status': 'error',
        'message': 'Token not provided or is invalid.'
    }

def test_it_should_return_flights(client):
    user = User(
        full_name='John Ade',
        phone_number='(324) 324 4234',
        address='1, afsfad, asdfasf.',
        email='johnade@gmail.com',
        password='password'
    )
    user.save()
    token = user.generate_token()

    flight = Flight(**{
        'estimated_arrival_time': '2014-12-22T03:12:58.019077+00:00',
        'airline': 'Arik',
        'departure_time': '2014-12-22T03:12:58.019077+00:00',
        'fare': 50000,
        'max_capacity': 1,
        'destination': 'Enugu',
        'origin': 'Calabar'
    })
    flight.save()

    response = client.get(
        '/v1/flights',
        headers={
            'Authorization': 'Bearer ' + token
        }
    )

    response_body = json.loads(response.data)

    assert response.status_code == 200
    assert response_body['status'] == 'success'
    assert any(response_flight['id'] == str(flight.id) for response_flight in response_body['data']['flights'])
    assert 'current_page' in response_body['data']['meta']
    assert 'limit' in response_body['data']['meta']
    assert 'total_items' in response_body['data']['meta']
    assert 'no_of_pages' in response_body['data']['meta']
