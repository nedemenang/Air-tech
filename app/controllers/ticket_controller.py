'''A controller module for flight-related
'''
from datetime import datetime
from app.controllers.base_controller import BaseController
from app.repositories.ticket_repo import TicketRepo
from app.repositories.flight_seat_repo import FlightSeatRepo
from app.repositories.flight_repo import FlightRepo
from app.repositories.user_repo import UserRepo
from app.utils.email import send_email
import string
import random


class TicketController(BaseController):
    def __init__(self, request):
        BaseController.__init__(self, request)
        self.ticket_repo = TicketRepo()
        self.flight_seat_repo = FlightSeatRepo()
        self.flight_repo = FlightRepo()
        self.user_repo = UserRepo()

    def get_tickets(self):
        tickets = self.ticket_repo.fetch_all()
        ticket_list = [ticket.serialize() for ticket in tickets.items]
        return self.handle_response('OK', payload={'tickets': ticket_list, 'meta': self.pagination_meta(tickets)})

    def get_ticket(self, ticket_id):
        ticket = self.ticket_repo.get(ticket_id)
        if ticket:
            ticket = ticket.serialize()
            return self.handle_response('OK', payload={'ticket': ticket})
        else:
            return self.handle_response('Bad Request - Invalid or missing ticketId', status_code=400)

    def create_ticket(self):
        flight_seat_id, status, user_id = self.request_params('flightSeatId', 'status', 'userId')
        flight_seat = self.flight_seat_repo.get(flight_seat_id)
        if flight_seat.is_available:
            ticket_no = ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
            ticket = self.ticket_repo.create_ticket(flight_seat_id, ticket_no, status, user_id)
            updates = {'is_available': False}
            self.flight_seat_repo.update(flight_seat, **updates)
            return self.handle_response('OK', payload={'ticket': ticket.serialize()})
        return self.handle_response('seat is unavailable', status_code=400)

    def update_ticket(self, ticket_id):
        flight_seat_id, status, user_id = self.request_params('flightSeatId', 'status', 'userId')
        ticket = self.ticket_repo.get(ticket_id)
        if ticket:
            updates = {}
            if flight_seat_id:
                updates['flight_seat_id'] = flight_seat_id
            if status:
                updates['status'] = status
            if user_id:
                updates['user_id'] = user_id

            if status == 'Booked':
                flight_seat = self.flight_seat_repo.filter_first(**{'id': flight_seat_id})
                flight = self.flight_repo.filter_first(**{'id': flight_seat.flight_id})
                user = self.user_repo.filter_first(**{'id': user_id})
                recipients = []
                recipients.append(user.email_address)
                send_email('Ticket Booked', 'airtech@email.com', recipients, flight, flight_seat, user, ticket)

            self.ticket_repo.update(ticket, **updates)
            return self.handle_response('OK', payload={'ticket': ticket.serialize()})
        return self.handle_response('Invalid or incorrect ticket_id provided', status_code=400)

    def delete_ticket(self, ticket_id):
        ticket = self.ticket_repo.get(ticket_id)
        updates = {}
        if ticket:
            updates['is_deleted'] = True

            self.ticket_repo.update(ticket, **updates)
            return self.handle_response('OK', payload={"status": "success"})
        return self.handle_response('Invalid or incorrect ticket_id provided', status_code=400)
