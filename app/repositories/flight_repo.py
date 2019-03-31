from app.repositories.base_repo import BaseRepo
from app.models.flight import Flight
from datetime import datetime


class FlightRepo(BaseRepo):

    def __init__(self):
        BaseRepo.__init__(self, Flight)

    def create_flight(self, flight_code, from_location, status, to_location, departure_date, departure_time, arrival_time, price, no_of_seats):
    
        flight = Flight(flight_code=flight_code, status=status, from_location=from_location, to_location=to_location, departure_date=departure_date, departure_time=departure_time, arrival_time=arrival_time, price=price, no_of_seats=no_of_seats)
        flight.save()
        return flight
