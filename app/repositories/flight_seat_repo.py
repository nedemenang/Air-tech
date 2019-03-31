from app.repositories.base_repo import BaseRepo
from app.models.flight_seats import FlightSeat
from datetime import datetime


class FlightSeatRepo(BaseRepo):

    def __init__(self):
        BaseRepo.__init__(self, FlightSeat)

    def create_flight_seat(self, flight_id, seat_number, is_available):
        flight_seat = FlightSeat(flight_id=flight_id, seat_number=seat_number, is_available=is_available)

        flight_seat.save()
        return flight_seat
