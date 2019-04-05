from test.base_test import BaseTestCase
import os
from app.utils import db
from test.factories.ticket_factory import TicketFactory
from test.factories.user_factory import UserFactory
from test.factories.flight_seat_factory import FlightSeatFactory
from test.factories.flight_factory import FlightFactory
from datetime import datetime, timedelta


class TicketEndpoint(BaseTestCase):

    def setUp(self):
        self.BaseSetUp()

    def test_create_ticket_endpoint(self):
        flight = FlightFactory.build()
        flight_seat = FlightSeatFactory.build(flight_id=flight.id)
        user = UserFactory.build()
        ticket = TicketFactory.build()

        db.session.add(flight)
        db.session.add(flight_seat)
        db.session.add(user)
        db.session.commit()

        data = {'flightSeatId': flight_seat.id, 'status': ticket.status, 'userId': user.id}
        response = self.client().post(self.make_url('/ticket/'), data=self.encode_to_json_string(data), headers=self.headers())
        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        payload = response_json['payload']

        self.assertJSONKeyPresent(response_json, 'payload')
        self.assertJSONKeyPresent(payload['ticket'], 'flightSeatId')
        self.assertJSONKeyPresent(payload['ticket'], 'ticketNo')

    def test_list_ticket_endpoint(self):
        flight = FlightFactory.build()
        flight_seat = FlightSeatFactory.build(flight_id=flight.id)
        user = UserFactory.build()
        
        db.session.add(flight)
        db.session.add(flight_seat)
        db.session.add(user)
        db.session.commit()

        ticket1 = TicketFactory.build(flight_seat_id=flight_seat.id, user_id=user.id, status="Booked")
        ticket2 = TicketFactory.build(flight_seat_id=flight_seat.id, user_id=user.id, status="PaidFor")
        db.session.add(ticket1)
        db.session.add(ticket2)
        db.session.commit()
        
        response = self.client().get(self.make_url('/ticket/'), headers=self.headers())
        response_json = self.decode_from_json_string(response.data.decode('utf-8'))
        payload = response_json['payload']
        print(payload['tickets'])
        self.assertJSONKeyPresent(response_json, 'payload')
        self.assertEqual(payload['tickets'][0]['ticketNo'], ticket1.ticket_no)
        self.assertEqual(payload['meta']['total_rows'], 2)

    def test_get_ticket_endpoint(self):
        flight = FlightFactory.build()
        flight_seat = FlightSeatFactory.build(flight_id=flight.id)
        user = UserFactory.build()
        
        db.session.add(flight)
        db.session.add(flight_seat)
        db.session.add(user)
        db.session.commit()

        ticket1 = TicketFactory.build(flight_seat_id=flight_seat.id, user_id=user.id, status="Booked")
        ticket2 = TicketFactory.build(flight_seat_id=flight_seat.id, user_id=user.id, status="PaidFor")
        db.session.add(ticket1)
        db.session.add(ticket2)
        db.session.commit()
        
        response = self.client().get(self.make_url('/ticket/{}/'.format(ticket1.id)), headers=self.headers())
        response_json = self.decode_from_json_string(response.data.decode('utf-8'))
        payload = response_json['payload']
        print(payload['ticket'])
        self.assertJSONKeyPresent(response_json, 'payload')
        self.assertEqual(payload['ticket']['ticketNo'], ticket1.ticket_no)

    def test_update_ticket_and_send_email_endpoint(self):
        flight = FlightFactory.build()
        flight_seat = FlightSeatFactory.build(flight_id=flight.id)
        user = UserFactory.build()
        
        db.session.add(flight)
        db.session.add(flight_seat)
        db.session.add(user)
        db.session.commit()

        ticket1 = TicketFactory.build(flight_seat_id=flight_seat.id, user_id=user.id, status="Reserved")
        db.session.add(ticket1)
        db.session.commit()
        
        data = {'flightSeatId': flight_seat.id, 'status': 'Booked', 'userId': user.id}
        print(ticket1.status)
        response = self.client().put(self.make_url('/ticket/{}/'.format(ticket1.id)), data=self.encode_to_json_string(data), headers=self.headers())
        response_json = self.decode_from_json_string(response.data.decode('utf-8'))
        payload = response_json['payload']
        # print(payload['ticket'])
        self.assertJSONKeyPresent(response_json, 'payload')
        self.assertEqual(payload['ticket']['status'], 'Booked')

    def test_delete_ticket_endpoint(self):
        flight = FlightFactory.build()
        flight_seat = FlightSeatFactory.build(flight_id=flight.id)
        user = UserFactory.build()
        
        db.session.add(flight)
        db.session.add(flight_seat)
        db.session.add(user)
        db.session.commit()

        ticket1 = TicketFactory.build(flight_seat_id=flight_seat.id, user_id=user.id, status="Reserved")
        db.session.add(ticket1)
        db.session.commit()
        
        data = {'flightSeatId': flight_seat.id, 'status': 'Booked', 'userId': user.id}
        response = self.client().delete(self.make_url('/ticket/{}/'.format(ticket1.id)), headers=self.headers())
        response_json = self.decode_from_json_string(response.data.decode('utf-8'))
        payload = response_json['payload']
        self.assertJSONKeyPresent(response_json, 'payload')
        self.assertEqual(payload['status'], 'success')
