from test.base_test import BaseTestCase
import os
from test.factories.location_factory import LocationFactory


class LocationEndpoints(BaseTestCase):

    def setUp(self):
        self.BaseSetUp()

    def test_create_location_endpoint(self):
        location = LocationFactory.build()
        data = {'locationCode': location.location_code, 'location': location.location}
        # print(self.make_url('/location'))
        response = self.client().post(self.make_url('/location/'), data=self.encode_to_json_string(data), headers=self.headers())
        response_json = self.decode_from_json_string(response.data.decode('utf-8'))
        print(response_json)
        print(self.headers())
        payload = response_json['payload']

        self.assertJSONKeyPresent(response_json, 'payload')
        self.assertEqual(payload['location']['locationCode'], location.location_code)
        self.assertEqual(payload['location']['location'], location.location)

    def test_list_location_endpoint(self):
        flights = LocationFactory.create_batch(3)
        response = self.client().get(self.make_url('/location/'), headers=self.headers())
        response_json = self.decode_from_json_string(response.data.decode('utf-8'))
        payload = response_json['payload']

        self.assert200(response)
        self.assertEqual(len(payload['locations']), 3)
        self.assertJSONKeysPresent(payload['locations'][0], 'locationCode', 'location')

    def test_get_specific_location_enpoint(self):
        location = LocationFactory.create()
        print('/location/{}/'.format(location.id))

        response = self.client().get(self.make_url('/location/{}/'.format(location.id)), headers=self.headers())
        response_json = self.decode_from_json_string(response.data.decode('utf-8'))
        payload = response_json['payload']

        self.assert200(response)
        self.assertJSONKeyPresent(payload, 'location')
        self.assertJSONKeysPresent(payload['location'], 'locationCode', 'location')
        self.assertEqual(int(payload['location']['id']), location.id)
        self.assertEqual(payload['location']['locationCode'], location.location_code)
        self.assertEqual(payload['location']['location'], location.location)

    def test_update_location_endpoint(self):
        location = LocationFactory.create()
        data = {'locationCode': 'ABV', 'location': 'Abuja'}
        response = self.client().put(self.make_url('/location/{}/'.format(location.id)), data=self.encode_to_json_string(data), headers=self.headers())
        response_json = self.decode_from_json_string(response.data.decode('utf-8'))
        payload = response_json['payload']

        self.assert200(response)
        self.assertEqual(payload['location']['locationCode'], data['locationCode'])
        self.assertEqual(payload['location']['location'], data['location'])
  

        '''Test invalid update request'''
        # User arbitrary value of 100 as the location ID
        response = self.client().put(self.make_url('/location/100/'), data=self.encode_to_json_string(data), headers=self.headers())
        self.assert400(response)

    def test_delete_location_endpoint(self):
        location = LocationFactory.create()

        response = self.client().delete(self.make_url('/location/{}/'.format(location.id)), headers=self.headers())
        response_json = self.decode_from_json_string(response.data.decode('utf-8'))
        payload = response_json['payload']
      
        self.assert200(response)
        self.assertEqual(payload['status'], "success")