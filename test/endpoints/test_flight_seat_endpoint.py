from test.base_test import BaseTestCase
import os
import time
from test.factories.flight_seat_factory import FlightSeatFactory
from test.factories.flight_factory import FlightFactory
from datetime import datetime, timedelta


class FlightSeatEndpoint(BaseTestCase):

    def setUp(self):
        self.BaseSetUp()

    def test_list_flight_seats_endpoint(self):
        flight = FlightFactory.build()
        data = {'flightCode': flight.flight_code, 'status': flight.status, 'fromLocation': flight.from_location, 'toLocation': flight.to_location, 'depatureTime': str(flight.departure_time), 'arrivalTime': str(flight.arrival_time), 'price': flight.price, 'noOfSeats': flight.no_of_seats, 'departureDate': str(flight.departure_date)}
        response = self.client().post(self.make_url('/flight/'), data=self.encode_to_json_string(data), headers=self.headers())
        response2 = self.client().get(self.make_url('/flightSeat/{}/'.format(flight.id)), headers=self.headers())
        response_json2 = self.decode_from_json_string(response2.data.decode('utf-8'))
        payload2 = response_json2['payload']
        self.assertJSONKeyPresent(response_json2, 'payload')

    def test_list_available_seats_endpoint(self):
        flight = FlightFactory.build()
        print(flight.id)
        data = {'flightCode': flight.flight_code, 'status': flight.status, 'fromLocation': flight.from_location, 'toLocation': flight.to_location, 'depatureTime': str(flight.departure_time), 'arrivalTime': str(flight.arrival_time), 'price': flight.price, 'noOfSeats': flight.no_of_seats, 'departureDate': str(flight.departure_date)}
        response = self.client().post(self.make_url('/flight/'), data=self.encode_to_json_string(data), headers=self.headers())
        response2 = self.client().get(self.make_url('/flightSeat/available/{}/'.format(flight.id)), headers=self.headers())
        response_json2 = self.decode_from_json_string(response2.data.decode('utf-8'))
        payload2 = response_json2['payload']
        self.assertJSONKeyPresent(response_json2, 'payload')

    def test_list_unavailable_seats_endpoint(self):
        flight = FlightFactory.build()
        data = {'flightCode': flight.flight_code, 'status': flight.status, 'fromLocation': flight.from_location, 'toLocation': flight.to_location, 'depatureTime': str(flight.departure_time), 'arrivalTime': str(flight.arrival_time), 'price': flight.price, 'noOfSeats': flight.no_of_seats, 'departureDate': str(flight.departure_date)}
        response = self.client().post(self.make_url('/flight/'), data=self.encode_to_json_string(data), headers=self.headers())
        response2 = self.client().get(self.make_url('/flightSeat/unavailable/{}/'.format(flight.id)), headers=self.headers())
        response_json2 = self.decode_from_json_string(response2.data.decode('utf-8'))
        payload2 = response_json2['payload']
        self.assertJSONKeyPresent(response_json2, 'payload')
    

