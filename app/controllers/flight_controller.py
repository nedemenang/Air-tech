'''A controller module for flight-related
'''
from datetime import datetime
from app import app
from threading import Thread
from app.controllers.base_controller import BaseController
from app.repositories.flight_repo import FlightRepo
from app.repositories.flight_seat_repo import FlightSeatRepo
from app.repositories.user_repo import UserRepo
from app.repositories.ticket_repo import TicketRepo
from dateutil import parser


class FlightController(BaseController):
    def __init__(self, request):
        BaseController.__init__(self, request)
        self.flight_repo = FlightRepo()
        self.user_repo = UserRepo()
        self.flight_seat_repo = FlightSeatRepo()
        self.ticket_repo = TicketRepo()

    def get_flights(self):
        flights = self.flight_repo.filter_by(**{'is_deleted': 'false'})
        flight_list = [flight.serialize() for flight in flights.items]
        return self.handle_response('OK', payload={'flights': flight_list, 'meta': self.pagination_meta(flights)})

    def get_available_seats(self, flight_id):
        flight_seats = self.flight_seat_repo.filter_by(**{'is_available': True, 'flight_id': flight_id})
        flight_seat_list = [flight_seat.serialize() for flight_seat in flight_seats.items]
        return self.handle_response('OK', payload={'flightSeats': flight_seat_list, 'meta': self.pagination_meta(flight_seats)})

    def get_users_booked_on_flight(self, flight_id):
        flight_seats = self.flight_seat_repo.filter_by(**{'is_available': False, 'flight_id': flight_id})
        seat_list = []
        for seat in flight_seats.items:
            serialize_seat = seat.serialize()
            ticket = self.ticket_repo.filter_first(**{'flight_seat_id': seat.id})
            user = self.user_repo.filter_first(**{'id': ticket.user_id})
            serialized_user = user.serialize()
            del serialized_user['password']
            serialize_seat['ticket'] = ticket.serialize()
            serialize_seat['user'] = serialized_user
            seat_list.append(serialize_seat)
        return self.handle_response('OK', payload={'flightSeats': seat_list, 'meta': self.pagination_meta(flight_seats)})

    def get_flights_by_location_and_date(self, from_location, to_location, departure_date):
        flights = self.flight_repo.filter_by(**{'from_location': from_location, 'to_location': to_location, 'departure_date': parser.parse(departure_date)})
        flight_list = [flight.serialize() for flight in flights.items]
        return self.handle_response('OK', payload={'flights': flight_list, 'meta': self.pagination_meta(flights)})

    def get_flights_by_location(self, from_location, to_location):
        flights = self.flight_repo.filter_by(**{'from_location': from_location, 'to_location': to_location})
        flight_list = [flight.serialize() for flight in flights.items]
        return self.handle_response('OK', payload={'flights': flight_list, 'meta': self.pagination_meta(flights)})

    def get_flight(self, flight_id):
        flight = self.flight_repo.get(flight_id)
        if flight:
            flight = flight.serialize()
            return self.handle_response('OK', payload={'flight': flight})
        else:
            return self.handle_response('Bad Request - Invalid or missing flight_id', status_code=400)

    def create_flight(self):
        flight_code, from_location, status, to_location, departure_time, arrival_time, price, no_of_seats = self.request_params('flightCode', 'fromLocation', 'status', 'toLocation', 'depatureTime', 'arrivalTime', 'price', 'noOfSeats')
        flight = self.flight_repo.create_flight(flight_code, from_location, status, to_location, datetime.date(parser.parse(departure_time)), departure_time, arrival_time, price, no_of_seats)
        Thread(target=self.create_flight_seat, args=(flight.id, no_of_seats)).start()
        return self.handle_response('OK', payload={'flight': flight.serialize()})

    def update_flight(self, flight_id):
        flight_code, from_location, to_location, status, departure_time, arrival_time, price, no_of_seats = self.request_params('flightCode', 'fromLocation', 'toLocation', 'status', 'depatureTime', 'arrivalTime', 'price', 'noOfSeats')

        flight = self.flight_repo.get(flight_id)
        if flight:
            updates = {}

            if flight_code:
                updates['flight_code'] = flight_code
            if from_location:
                updates['from_location'] = from_location
            if to_location:
                updates['to_location'] = to_location
            if status:
                updates['status'] = status
            if departure_time:
                updates['departure_time'] = departure_time
                updates['departure_date'] = datetime.date(departure_time)
            if arrival_time:
                updates['arrival_time'] = arrival_time
            if price:
                updates['price'] = price
            if no_of_seats:
                updates['no_of_seats'] = no_of_seats
            self.flight_repo.update(flight, **updates)
            return self.handle_response('OK', payload={'status': 'success', 'flight': flight.serialize()})
        return self.handle_response('Invalid or incorrect flight_id provided', status_code=400)

    def delete_flight(self, flight_id):
        flight = self.flight_repo.get(flight_id)
        updates = {}
        if flight:
            updates['is_deleted'] = True

            self.flight_repo.update(flight, **updates)
            return self.handle_response('OK', payload={'status': 'success'})
        return self.handle_response('Invalid or incorrect flight_id provided', status_code=400)

    def create_flight_seat(self, flight_id, no_of_seats):
        with app.app_context():
            seats = self._generate_seat_number(no_of_seats)
            for seat in seats:
                self.flight_seat_repo.create_flight_seat(flight_id, seat, True)

    def _generate_seat_number(self, no_of_seats):
            letters = ['A', 'B', 'C', 'D', 'E', 'F']
            seat_list = []
            count = 1
            for i in range(1, int(int(no_of_seats)/len(letters))):
                for m in letters:
                    seat_list.append(m+str(count))
                count += 1
            return seat_list
