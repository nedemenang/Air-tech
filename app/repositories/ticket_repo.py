from app.repositories.base_repo import BaseRepo
from app.models.ticket import Ticket
from datetime import datetime


class TicketRepo(BaseRepo):

    def __init__(self):
        BaseRepo.__init__(self, Ticket)

    def create_ticket(self, flight_seat_id, ticket_no, status, user_id):
        ticket = Ticket(flight_seat_id=flight_seat_id, ticket_no=ticket_no, status=status, user_id=user_id)

        ticket.save()
        return ticket
