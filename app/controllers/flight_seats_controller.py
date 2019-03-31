from app.controllers.base_controller import BaseController
from app.repositories.flight_seat_repo import FlightSeatRepo


class FlightSeatController(BaseController):
    def __init__(self, request):
        BaseController.__init__(self, request)
        self.flight_seat_repo = FlightSeatRepo()

    def get_all_seats_on_flight(self, flight_id):
        flight_seats = self.flight_seat_repo.filter_by(**{'flight_id': flight_id})
        flight_seats_list = [flight_seat.serialize() for flight_seat in flight_seats.items]
        return self.handle_response('OK', payload={'flightSeats': flight_seats_list, 'meta': self.pagination_meta(flight_seats)})

    def get_available_seats_on_flight(self, flight_id):
        flight_seats = self.flight_seat_repo.filter_by(**{'flight_id': flight_id, 'is_available': True})
        flight_seats_list = [flight_seat.serialize() for flight_seat in flight_seats.items]
        return self.handle_response('OK', payload={'flightSeats': flight_seats_list, 'meta': self.pagination_meta(flight_seats)})

    def get_unavailable_seats_on_flight(self, flight_id):
        flight_seats = self.flight_seat_repo.filter_by(**{'flight_id': flight_id, 'is_available': False})
        flight_seats_list = [flight_seat.serialize() for flight_seat in flight_seats.items]
        return self.handle_response('OK', payload={'flightSeats': flight_seats_list, 'meta': self.pagination_meta(flight_seats)})

