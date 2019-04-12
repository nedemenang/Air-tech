import celery
from datetime import datetime, timedelta
from app import app
from app.repositories.ticket_repo import TicketRepo
from app.repositories.flight_seat_repo import FlightSeatRepo
from app.repositories.flight_repo import FlightRepo
from app.repositories.user_repo import UserRepo
from app.repositories.ticket_repo import TicketRepo
from app.utils.email import send_email


@celery.task()
def check_and_send_email():
    with app.app_context():
        flight_repo = FlightRepo()
        print("Searching records....")
        flights = flight_repo.filter_by(**{'is_deleted': 'false', 'departure_time': (datetime.now() + timedelta(days=1)).strftime('%B %d, %Y %H:%M')})
        if flights:
            flight_seat_repo = FlightSeatRepo()
            user_repo = UserRepo()
            ticket_repo = TicketRepo()
            for flight in flights.items:
                flight_seats = flight_seat_repo.filter_by(**{'flight_id': flight.id, 'is_available': False})
                for flight_seat in flight_seats.items:
                    ticket = ticket_repo.filter_first(**{'flight_seat_id': flight_seat.id, 'is_deleted': False})
                    user = user_repo.filter_first(**{'id': ticket.user_id})
                    print("Sending email....")
                    send_email('Flight Reminder', 'airtech@email.com', [user.email_address], flight, flight_seat, user, ticket)
