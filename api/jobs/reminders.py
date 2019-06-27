from datetime import datetime, timedelta
from sendgrid import SendGridAPIClient
from decouple import config as env_config

from api.models.flight import Flight
from api.models.flight_ticket import FlightTicket
from api.constants import flight_statuses

def remind_users_of_upcoming_flights():
    sg = SendGridAPIClient(env_config('SENDGRID_KEY'))

    tomorrow = datetime.now() + timedelta(days=1)
    pending_flights = Flight.objects(
        departure_time__gte=tomorrow.replace(hour=0, minute=0),
        departure_time__lte=tomorrow.replace(hour=23, minute=59),
        status=flight_statuses.PENDING
    )

    booked_tickets = FlightTicket.objects(
        flight__in=pending_flights
    )

    for ticket in booked_tickets:
        message = {
            'personalizations': [
                {
                    'to': [
                        {
                            'email': ticket.user.email
                        }
                    ],
                    'subject': 'Flight reminder'
                }
            ],
            'from': {
                'email': 'reminder@flightbooker.com',
                'name': 'Flight Booker'
            },
            'content': [
                {
                    'type': 'text/plain',
                    'value': '''
                        Hi {0}, \n\nThis is a reminder of your flight scheduled to depart tomorrow by {1}.
                    '''.format(
                        ticket.user.full_name,
                        ticket.flight.departure_time.strftime('%-I:%M %p')
                    )
                }
            ]
        }

        sg.send(message)
