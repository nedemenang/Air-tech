import celery
from datetime import datetime, timedelta
from app.repositories.ticket_repo import TicketRepo
from app.repositories.flight_seat_repo import FlightSeatRepo
from app.repositories.flight_repo import FlightRepo
from app.repositories.user_repo import UserRepo
from app.repositories.ticket_repo import TicketRepo
from app.utils.email import send_email


@celery.task()
def check_and_send_email(self):
    logger = check_and_send_email.get_logger()
    logger.info("Searching records....")
    flights = FlightRepo.filter_by(**{'departure_time': datetime.now() + timedelta(hours=24)})
    if flights:
        for flight in flights:
            flight_seats = FlightSeatRepo.filter_by(**{'flight_id': flight.id, 'is_available': False})
            for flight_seat in flight_seats:
                user = UserRepo.filter_first(**{'id': flight_seat.user_id})
                ticket = TicketRepo.filter_first(**{'flight_seat_id': flight_seat.id})
                logger.info("Sending email....")
                send_email('Flight Reminder', 'airtech@email.com', [user.email_address], flight, flight_seat, user, ticket)
