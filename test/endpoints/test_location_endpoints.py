from test.base_test import BaseTestCase
from test.factories.location_factory import LocationFactory


class LocationEndpoints(BaseTestCase):

    def setUp(self):
        self.BaseSetUp()

    def test_create_location_endpoint(self):
        location = LocationFactory.build()
        data = {'locationCode': location.location_code, 'location': location.location}
        response = self.client().post(self.make_url('location'), data=self.encode_to_json_string(data), headers=self.headers())
        response_json = self.decode_from_json_string(response.data.decode('utf-8'))
        payload = response_json['payload']

        self.assert200(response)
        self.assertJSONKeyPresent(response_json, 'payload')
        self.assertEqual(payload['location']['locationCode'], location.location_code)
        self.assertEqual(payload['location']['location'], location.location)
