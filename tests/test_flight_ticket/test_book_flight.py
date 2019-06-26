import json

from api.models.user import User
from api.models.flight import Flight
from api.models.flight_ticket import FlightTicket

def test_it_return_401_if_authorization_header_is_not_passed(client):
    response = client.post(
        '/v1/flights/asdfasfasd/book',
        data=json.dumps({})
    )

    response_body = json.loads(response.data)

    assert response.status_code == 401
    assert response_body == {
        'status': 'error',
        'message': 'Token not provided or is invalid.'
    }

def test_it_should_return_404_if_flight_id_is_invalid(client):
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
        '/v1/flights/asdfasfasd/book',
        data=json.dumps({}),
        headers={
            'Authorization': 'Bearer ' + token
        }
    )

    response_body = json.loads(response.data)

    assert response.status_code == 404
    assert response_body == {
        'status': 'error',
        'message': 'Flight not found.'
    }

def test_it_should_return_404_if_flight_is_not_found(client):
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
        '/v1/flights/{}/book'.format(str(user.id)),
        data=json.dumps({}),
        headers={
            'Authorization': 'Bearer ' + token
        }
    )

    response_body = json.loads(response.data)

    assert response.status_code == 404
    assert response_body == {
        'status': 'error',
        'message': 'Flight not found.'
    }

def test_it_should_create_flight_ticket_if_booking_is_successful(client):
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
        'max_capacity': 40,
        'destination': 'Enugu',
        'origin': 'Calabar'
    })
    flight.save()

    response = client.post(
        '/v1/flights/{}/book'.format(str(flight.id)),
        data=json.dumps({}),
        headers={
            'Authorization': 'Bearer ' + token
        }
    )

    response_body = json.loads(response.data)

    assert response.status_code == 201
    assert response_body['status'] == 'success'
    assert response_body['data']['flight_ticket']['flight']['id'] == str(flight.id)
    assert 'ticket_number' in response_body['data']['flight_ticket']
    assert 'password' not in response_body['data']['flight_ticket']['user']



def test_it_should_return_422_if_flight_is_full(client):
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

    flight_ticket = FlightTicket(
        user=user,
        flight=flight
    )
    flight_ticket.save()

    response = client.post(
        '/v1/flights/{}/book'.format(str(flight.id)),
        data=json.dumps({}),
        headers={
            'Authorization': 'Bearer ' + token
        }
    )

    response_body = json.loads(response.data)

    assert response.status_code == 422
    assert response_body == {
        'status': 'error',
        'message': 'Flight is full and cannot be booked'
    }
