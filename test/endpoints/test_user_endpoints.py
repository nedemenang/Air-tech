from test.base_test import BaseTestCase
import os
from test.factories.user_factory import UserFactory
from app import bcrypt


class UserEndpoints(BaseTestCase):

    def setUp(self):
        self.BaseSetUp()

    def test_create_user_endpoint(self):
        user = UserFactory.build()
        data = {'firstName': user.first_name, 'lastName': user.last_name, 'middleName': user.middle_name, 'emailAddress': user.email_address, 'password': user.password}
        response = self.client().post(self.make_url('/user/'), data=self.encode_to_json_string(data), headers=self.headers())
        response_json = self.decode_from_json_string(response.data.decode('utf-8'))
        payload = response_json['payload']

        self.assertJSONKeyPresent(response_json, 'payload')
        self.assertEqual(payload['user']['firstName'], user.first_name)
        self.assertEqual(payload['user']['lastName'], user.last_name)
        self.assertEqual(payload['user']['middleName'], user.middle_name)
        self.assertEqual(payload['user']['emailAddress'], user.email_address)

    def test_create_user_invalid_email_endpoint(self):
        user = UserFactory.build()
        data = {'firstName': user.first_name, 'lastName': user.last_name, 'middleName': user.middle_name, 'emailAddress': user.first_name, 'password': user.password}
        response = self.client().post(self.make_url('/user/'), data=self.encode_to_json_string(data), headers=self.headers())
        response_json = self.decode_from_json_string(response.data.decode('utf-8'))
        payload = response_json['msg']

        self.assertJSONKeyPresent(response_json, 'msg')
        self.assertEqual(payload, 'Bad Request - enter valid email address')

    def test_create_user_weak_password_endpoint(self):
        user = UserFactory.build()
        data = {'firstName': user.first_name, 'lastName': user.last_name, 'middleName': user.middle_name, 'emailAddress': user.email_address, 'password': 'weakpassword'}
        response = self.client().post(self.make_url('/user/'), data=self.encode_to_json_string(data), headers=self.headers())
        response_json = self.decode_from_json_string(response.data.decode('utf-8'))
        payload = response_json['msg']

        self.assertJSONKeyPresent(response_json, 'msg')
        self.assertEqual(payload, 'Bad Request - password not strong enough')

    def test_login_endpoint(self):
        user = UserFactory.create()

        data = {'emailAddress': user.email_address, 'password': 'Password1'}
        response = self.client().post(self.make_url('/user/login'), data=self.encode_to_json_string(data), headers=self.headers())
        response_json = self.decode_from_json_string(response.data.decode('utf-8'))
        payload = response_json['payload']

        self.assertJSONKeyPresent(response_json, 'payload')
        self.assertEqual(payload['user']['firstName'], user.first_name)
        self.assertEqual(payload['user']['lastName'], user.last_name)
        self.assertEqual(payload['user']['middleName'], user.middle_name)
        self.assertEqual(payload['user']['emailAddress'], user.email_address)

    def test_reset_with_weak_password_endpoint(self):
        user = UserFactory.create()

        data = {'emailAddress': user.email_address, 'password': 'weakpassword'}
        response = self.client().put(self.make_url('/user/reset'), data=self.encode_to_json_string(data), headers=self.headers())
        response_json = self.decode_from_json_string(response.data.decode('utf-8'))
        payload = response_json['msg']

        self.assertJSONKeyPresent(response_json, 'msg')
        self.assertEqual(payload, 'Bad Request - password not strong enough')

    def test_reset_with_strong_password_endpoint(self):
        user = UserFactory.create()
        password = 'StrongPassword@123'
        data = {'emailAddress': user.email_address, 'password': password}
        response = self.client().put(self.make_url('/user/reset'), data=self.encode_to_json_string(data), headers=self.headers())
        response_json = self.decode_from_json_string(response.data.decode('utf-8'))
        payload = response_json['msg']

        self.assertJSONKeyPresent(response_json, 'msg')
        self.assertEqual(payload, 'OK')


