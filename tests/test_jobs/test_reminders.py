from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock
from api.jobs import reminders

class MockClass(object):
    pass

mock_sg = MockClass()
mock_sg.send = MagicMock()

def mock_flight_ticket_objects_method():
    mock_ticket = MockClass()
    mock_ticket.user = MockClass()
    mock_ticket.user.email = 'test@gmail.com'
    mock_ticket.user.full_name = 'Test User'
    mock_ticket.flight = MockClass()
    mock_ticket.flight.departure_time = datetime.strptime('2019-06-27', '%Y-%m-%d')

    objects_mock = MagicMock()
    objects_mock.return_value = [mock_ticket]

    return objects_mock

@patch('api.jobs.reminders.FlightTicket.objects', new_callable=mock_flight_ticket_objects_method)
@patch('api.jobs.reminders.Flight')
@patch('api.jobs.reminders.env_config', return_value='sendgrid_key')
@patch('api.jobs.reminders.SendGridAPIClient', return_value=mock_sg)
def test_remind_users_of_upcoming_flights(
    SendGridAPIClient,
    env_config,
    Flight,
    FlightTicketObjects):

    reminders.remind_users_of_upcoming_flights()

    env_config.assert_called_with('SENDGRID_KEY')
    SendGridAPIClient.assert_called_with('sendgrid_key')

    Flight.objects.assert_called()
    FlightTicketObjects.assert_called()


