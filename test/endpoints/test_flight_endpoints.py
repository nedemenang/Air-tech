from test.base_test import BaseTestCase
import os
from test.factories.flight_factory import FlightFactory
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
        data = {'flightCode': 'ARK2102', 'status': 'OnTime', 'fromLocation': 'ABV', 'toLocation': 'LOS', 'depatureTime': str(datetime.now()), 'arrivalTime': str(datetime.now()+timedelta(hours=1)), 'price': 35000, 'noOfSeats': 150}
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
    

