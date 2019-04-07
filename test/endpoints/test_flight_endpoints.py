from test.base_test import BaseTestCase
import os
from app.utils import db
from test.factories.flight_factory import FlightFactory
from test.factories.flight_seat_factory import FlightSeatFactory
from test.factories.ticket_factory import TicketFactory
from test.factories.user_factory import UserFactory
from datetime import datetime, timedelta


class FlightEndpoint(BaseTestCase):

    def setUp(self):
        self.BaseSetUp()

    def test_create_flight_endpoint(self):
        flight = FlightFactory.build()
        data = {'flightCode': flight.flight_code, 'status': flight.status, 'fromLocation': flight.from_location, 'toLocation': flight.to_location, 'depatureTime': str(flight.departure_time), 'arrivalTime': str(flight.arrival_time), 'price': flight.price, 'noOfSeats': flight.no_of_seats, 'departureDate': str(flight.departure_date)}
        response = self.client().post(self.make_url('/flight/'), data=self.encode_to_json_string(data), headers=self.headers())
        response_json = self.decode_from_json_string(response.data.decode('utf-8'))
        payload = response_json['payload']

        self.assertJSONKeyPresent(response_json, 'payload')
        self.assertEqual(payload['flight']['flightCode'], flight.flight_code)
        self.assertEqual(payload['flight']['fromLocation'], flight.from_location)
        self.assertEqual(payload['flight']['toLocation'], flight.to_location)
        self.assertEqual(payload['flight']['noOfSeats'], flight.no_of_seats)

    def test_create_flight_validation_endpoint(self):
        flight = FlightFactory.build()
        data = {'flightCode': '', 'status': flight.status, 'fromLocation': flight.from_location, 'toLocation': flight.to_location, 'depatureTime': str(flight.departure_time), 'arrivalTime': str(flight.arrival_time), 'price': flight.price, 'noOfSeats': flight.no_of_seats, 'departureDate': str(flight.departure_date)}
        response = self.client().post(self.make_url('/flight/'), data=self.encode_to_json_string(data), headers=self.headers())
        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assert400(response)

    def test_create_flight_price_validation_endpoint(self):
        flight = FlightFactory.build()
        data = {'flightCode': '', 'status': flight.status, 'fromLocation': flight.from_location, 'toLocation': flight.to_location, 'depatureTime': str(flight.departure_time), 'arrivalTime': str(flight.arrival_time), 'price': 'flight.price', 'noOfSeats': flight.no_of_seats, 'departureDate': str(flight.departure_date)}
        response = self.client().post(self.make_url('/flight/'), data=self.encode_to_json_string(data), headers=self.headers())
        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assert400(response)

    def test_list_users_booked_on_flights_endpoint(self):
        flight = FlightFactory.build()
        flight_seat1 = FlightSeatFactory.build(flight_id=flight.id, is_available=False)
        flight_seat2 = FlightSeatFactory.build(flight_id=flight.id, is_available=False)
        user1 = UserFactory.build()
        user2 = UserFactory.build()
        
        db.session.add(flight)
        db.session.add(flight_seat1)
        db.session.add(flight_seat2)
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()

        ticket1 = TicketFactory.build(flight_seat_id=flight_seat1.id, user_id=user1.id, status="PaidFor")
        ticket2 = TicketFactory.build(flight_seat_id=flight_seat2.id, user_id=user2.id, status="PaidFor")
        db.session.add(ticket1)
        db.session.add(ticket2)
        db.session.commit()
        
        response = self.client().get(self.make_url('/flight/reserved/{}/'.format(flight.id)), headers=self.headers())
        response_json = self.decode_from_json_string(response.data.decode('utf-8'))
        payload = response_json['payload']
        print(response_json)
        self.assertJSONKeyPresent(response_json, 'payload')
        self.assertEqual(len(payload['flightSeats']), 2)



    def test_list_flight_endpoint(self):
        flights = FlightFactory.create_batch(3)
        response = self.client().get(self.make_url('/flight/'), headers=self.headers())
        response_json = self.decode_from_json_string(response.data.decode('utf-8'))
        payload = response_json['payload']

        self.assert200(response)
        self.assertEqual(len(payload['flights']), 3)
        self.assertJSONKeysPresent(payload['flights'][0], 'flightCode', 'fromLocation')
        self.assertEqual(payload['flights'][0]['flightCode'], flights[0].flight_code)
        self.assertEqual(payload['flights'][0]['fromLocation'], flights[0].from_location)
        self.assertEqual(payload['flights'][0]['toLocation'], flights[0].to_location)

    def test_get_specific_flight_endpoint(self):
        flight = FlightFactory.create()
        response = self.client().get(self.make_url('/flight/{}/'.format(flight.id)), headers=self.headers())
        response_json = self.decode_from_json_string(response.data.decode('utf-8'))
        payload = response_json['payload']
        print(payload)

        self.assert200(response)
        self.assertJSONKeysPresent(payload['flight'], 'flightCode', 'fromLocation')
        self.assertEqual(payload['flight']['flightCode'], flight.flight_code)
        self.assertEqual(payload['flight']['fromLocation'], flight.from_location)
        self.assertEqual(payload['flight']['toLocation'], flight.to_location)

    def test_get_flight_by_location_and_date_endpoint(self):
        flight = FlightFactory.create_batch(5)
        response = self.client().get(self.make_url('/flight/{}/{}/{}/'.format(flight[2].from_location, flight[2].to_location, flight[2].departure_date)), headers=self.headers())
        response_json = self.decode_from_json_string(response.data.decode('utf-8'))
        payload = response_json['payload']

        self.assert200(response)
        self.assertJSONKeysPresent(payload['flights'][2], 'flightCode', 'fromLocation')
        self.assertEqual(payload['flights'][2]['flightCode'], flight[2].flight_code)
        self.assertEqual(payload['flights'][2]['fromLocation'], flight[2].from_location)
        self.assertEqual(payload['flights'][2]['toLocation'], flight[2].to_location)

    def test_update_flight_endpoint(self):
        flight = FlightFactory.create()
        data = {'flightCode': 'ARK2102', 'status': 'TakenOff', 'fromLocation': 'ABV', 'toLocation': 'LOS', 'depatureTime': str(datetime.now()), 'arrivalTime': str(datetime.now()+timedelta(hours=1)), 'price': 35000, 'noOfSeats': 150}
        response = self.client().put(self.make_url('/flight/{}/'.format(flight.id)), data=self.encode_to_json_string(data), headers=self.headers())
        response_json = self.decode_from_json_string(response.data.decode('utf-8'))
        payload = response_json['payload']

        self.assert200(response)
        self.assertEqual(payload['flight']['flightCode'], data['flightCode'])
        self.assertEqual(payload['flight']['fromLocation'], data['fromLocation'])
        self.assertEqual(payload['flight']['toLocation'], data['toLocation'])

    def test_delete_flight_endpoint(self):
        flight = FlightFactory.create()
        response = self.client().delete(self.make_url('/flight/{}/'.format(flight.id)), headers=self.headers())
        response_json = self.decode_from_json_string(response.data.decode('utf-8'))
        payload = response_json['payload']

        self.assert200(response)
        self.assertEqual(payload['status'], "success")
    

