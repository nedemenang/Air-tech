from test.base_test import BaseTestCase
import os
from app.utils import db

from test.factories.user_factory import UserFactory
from test.factories.card_factory import CardFactory


class CardEndpoints(BaseTestCase):

    def setUp(self):
        self.BaseSetUp()

    def test_create_card_endpoint(self):
        user = UserFactory.build()
        print(user.first_name)
        db.session.add(user)
        db.session.commit()

        card = CardFactory.build(user_id=user.id)
        data = {'cardNumber': card.card_number, 'expiryMonth': card.expiry_month, 'expiryYear': card.expiry_year, 'securityNumber': card.securiy_number, 'userId': user.id}

        response = self.client().post(self.make_url('/card/'), data=self.encode_to_json_string(data), headers=self.headers())
        response_json = self.decode_from_json_string(response.data.decode('utf-8'))
        print(response_json)
        payload = response_json['payload']

        self.assertJSONKeyPresent(response_json, 'payload')
        self.assertEqual(payload['cardDetail']['cardNumber'], card.card_number)
        self.assertEqual(payload['cardDetail']['securiyNumber'], int(card.securiy_number))

    def test_create_card_validation_endpoint(self):
        user = UserFactory.build()
        print(user.first_name)
        db.session.add(user)
        db.session.commit()

        card = CardFactory.build(user_id=user.id)
        data = {'cardNumber': 2, 'expiryMonth': 'card.expiry_month', 'expiryYear': 'card.expiry_year', 'securityNumber': card.securiy_number, 'userId': user.id}

        response = self.client().post(self.make_url('/card/'), data=self.encode_to_json_string(data), headers=self.headers())
        response_json = self.decode_from_json_string(response.data.decode('utf-8'))

        self.assert400(response)
        

    def test_list_card_endpoint(self):
        user = UserFactory.build()

        db.session.add(user)
        db.session.commit()

        card1 = CardFactory.build(user_id=user.id)
        card2 = CardFactory.build(user_id=user.id)
        db.session.add(card1)
        db.session.add(card2)
        db.session.commit()

        response = self.client().get(self.make_url('/card/'), headers=self.headers())
        response_json = self.decode_from_json_string(response.data.decode('utf-8'))
        payload = response_json['payload']

        self.assert200(response)
        self.assertEqual(len(payload['cardDetails']), 2)
        self.assertJSONKeysPresent(payload['cardDetails'][0], 'cardNumber', 'expiryMonth')

    def test_get_specific_card_enpoint(self):
        user = UserFactory.build()

        db.session.add(user)
        db.session.commit()

        card = CardFactory.build(user_id=user.id)
        db.session.add(card)

        db.session.commit()

        response = self.client().get(self.make_url('/card/{}/'.format(card.id)), headers=self.headers())
        response_json = self.decode_from_json_string(response.data.decode('utf-8'))
        payload = response_json['payload']

        self.assert200(response)
        self.assertJSONKeyPresent(payload, 'cardDetail')
        self.assertJSONKeysPresent(payload['cardDetail'], 'cardNumber', 'securiyNumber')
        self.assertEqual(int(payload['cardDetail']['id']), card.id)
        self.assertEqual(payload['cardDetail']['securiyNumber'], int(card.securiy_number))
        self.assertEqual(payload['cardDetail']['cardNumber'], card.card_number)

    def test_update_card_endpoint(self):
        user = UserFactory.build()

        db.session.add(user)
        db.session.commit()

        card = CardFactory.build(user_id=user.id)
        db.session.add(card)

        db.session.commit()

        data = data = {'cardNumber': '1234567890987665', 'expiryMonth': '3', 'expiryYear': '2026', 'securityNumber': '123'}
        response = self.client().put(self.make_url('/card/{}/'.format(card.id)), data=self.encode_to_json_string(data), headers=self.headers())
        response_json = self.decode_from_json_string(response.data.decode('utf-8'))
        payload = response_json['payload']

        self.assert200(response)
        self.assertEqual(payload['cardDetail']['securiyNumber'], int(card.securiy_number))
        self.assertEqual(payload['cardDetail']['cardNumber'], card.card_number)
  

        '''Test invalid update request'''
        # User arbitrary value of 100 as the location ID
        response = self.client().put(self.make_url('/card/100/'), data=self.encode_to_json_string(data), headers=self.headers())
        self.assert400(response)

    def test_delete_card_endpoint(self):
        user = UserFactory.build()

        db.session.add(user)
        db.session.commit()

        card = CardFactory.build(user_id=user.id)
        db.session.add(card)

        db.session.commit()
        response = self.client().delete(self.make_url('/card/{}/'.format(card.id)), headers=self.headers())
        response_json = self.decode_from_json_string(response.data.decode('utf-8'))
        payload = response_json['payload']
      
        self.assert200(response)
        self.assertEqual(payload['status'], "success")