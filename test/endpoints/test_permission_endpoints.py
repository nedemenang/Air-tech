import datetime
from test.base_test import BaseTestCase
from app.repositories.role_repo import RoleRepo
from test.factories.permission_factory import PermissionFactory, RoleFactory, UserRoleFactory
# from .user_role import create_user_role
# from unittest.mock import Mock, patch


class TestRoleEndpoints(BaseTestCase):
    
    def setUp(self):
        self.BaseSetUp()

    def test_get_role_permissions_list_endpoint(self):

        response = self.client().get(self.make_url('/permission/permissions/1'), headers=self.headers())
        
        response_json = self.decode_from_json_string(response.data.decode('utf-8'))
        payload = response_json['payload']

        self.assertEqual(response.status_code, 200)
        self.assertJSONKeyPresent(response_json, 'payload')