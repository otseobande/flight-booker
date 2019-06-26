import json, datetime

from api.models.user import User
from api.models.flight import Flight
from api.models.flight_ticket import FlightTicket

def test_it_return_401_if_authorization_header_is_not_passed(client):
    response = client.get(
        '/v1/flights/asdfasfasd/bookings',
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

    response = client.get(
        '/v1/flights/asdfasfasd/bookings',
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

    response = client.get(
        '/v1/flights/{}/bookings'.format(str(user.id)),
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

def test_it_should_return_error_if_date_is_invalid(client):
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
        '/v1/flights/{}/bookings?date=2012'.format(str(flight.id)),
        headers={
            'Authorization': 'Bearer ' + token
        }
    )

    response_body = json.loads(response.data)

    assert response.status_code == 400
    assert response_body == {
        'status': 'error',
        'message': 'Date should be in YYYY-MM-DD format'
    }

def test_it_should_return_flight_bookings_successfully_if_date_is_passed(client):
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

    response = client.get(
        '/v1/flights/{0}/bookings?date={1}'.format(
            str(flight.id),
            datetime.datetime.today().strftime('%Y-%m-%d')
        ),
        headers={
            'Authorization': 'Bearer ' + token
        }
    )

    response_body = json.loads(response.data)

    assert response.status_code == 200
    assert response_body['status'] == 'success'
    assert any(response_flight_ticket['id'] == str(flight_ticket.id) for response_flight_ticket in response_body['data']['flight_tickets'])
    assert 'current_page' in response_body['data']['meta']
    assert 'limit' in response_body['data']['meta']
    assert 'total_items' in response_body['data']['meta']
    assert 'no_of_pages' in response_body['data']['meta']


def test_it_should_return_flight_bookings_for_the_day_without_date_successfully(client):
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

    response = client.get(
        '/v1/flights/{0}/bookings'.format(
            str(flight.id),
        ),
        headers={
            'Authorization': 'Bearer ' + token
        }
    )

    response_body = json.loads(response.data)

    assert response.status_code == 200
    assert response_body['status'] == 'success'
    assert any(response_flight_ticket['id'] == str(flight_ticket.id) for response_flight_ticket in response_body['data']['flight_tickets'])
    assert 'current_page' in response_body['data']['meta']
    assert 'limit' in response_body['data']['meta']
    assert 'total_items' in response_body['data']['meta']
    assert 'no_of_pages' in response_body['data']['meta']


def test_it_should_return_flight_bookings_successfully_if_pagination_params_are_invalid(client):
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

    response = client.get(
        '/v1/flights/{0}/bookings?page='.format(
            str(flight.id),
        ),
        headers={
            'Authorization': 'Bearer ' + token
        }
    )

    response_body = json.loads(response.data)

    assert response.status_code == 200
    assert response_body['status'] == 'success'
    assert any(response_flight_ticket['id'] == str(flight_ticket.id) for response_flight_ticket in response_body['data']['flight_tickets'])
    assert 'current_page' in response_body['data']['meta']
    assert 'limit' in response_body['data']['meta']
    assert 'total_items' in response_body['data']['meta']
    assert 'no_of_pages' in response_body['data']['meta']
