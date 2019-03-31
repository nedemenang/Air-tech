import jwt
from functools import wraps
from config import get_env
from datetime import datetime, timedelta
from flask import request, jsonify, make_response
from app.repositories.permission_repo import PermissionRepo
from app.repositories.user_role_repo import UserRoleRepo


class Auth:

    authentication_header_ignore = [
        '/login', '/'
    ]

    @staticmethod
    def check_token():

        if request.method != 'OPTIONS':
            for endpoint in Auth.authentication_header_ignore:
                if request.path.find(endpoint) > -1:
                    return None
            try:
                token = Auth.get_token()
            except Exception as e:
                return make_response(jsonify({'msg': str(e)}), 400)

            try:
                decoded = Auth.decode_token(token)
            except Exception as e:
                return make_response(jsonify({'msg': str(e)}), 400)

    @staticmethod
    def create_token(user_id):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.now() + timedelta(days=0, seconds=120),
                'iat': datetime.now(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                get_env('SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            print(str(e))
            return e

    @staticmethod
    def get_token(request_obj=None):
        if request_obj:
            header = request_obj.headers.get('Authorization', None)
        else:
            header = request.headers.get('Authorization', None)
        if not header:
            raise Exception('Authorization Header is Expected')

        header_parts = header.split()

        if header_parts[0].lower() != 'bearer':
            raise Exception('Authorization header must start with bearer')
        elif len(header_parts) > 1:
            return header_parts[1]

        raise Exception('Internal application error')

    @staticmethod
    def decode_token(token):
        try:
            jwtsecret = get_env('SECRET_KEY')
            decoded = jwt.decode(token, jwtsecret)
            return decoded
        except jwt.ExpiredSignature:
            return make_response(jsonify({'msg': 'Token is expired'})), 400
        except jwt.DecodeError:
            raise Exception('Error decoding')

    @staticmethod
    def _get_user():
        token = None
        try:
            token = Auth.get_token()
        except Exception as e:
            print(str(e))
            raise e

        try:
            if token:
                return Auth.decode_token(token)
        except Exception as e:
            print(str(e))
            raise e

    @staticmethod
    def user(*keys):
        user = Auth._get_user()
        if keys:
            if len(keys) > 1:
                values = list()
                for key in keys:
                    values.append(user[key]) if key in user else values.append(None)
                return values
            if len(keys) == 1 and keys[0] in user:
                return user[keys[0]]

    @staticmethod
    def has_permission(permission):
        def permission_checker(f):

            @wraps(f)
            def decorated(*args, **kwargs):

                user_role_repo = UserRoleRepo()
                permission_repo = PermissionRepo()

                user_id = Auth.user('sub')
                user_role = user_role_repo.find_first(**{'user_id': user_id})

                if not user_id:
                    return make_response(jsonify({'msg': 'Missing user ID in token'})), 400

                if not user_role:
                    return make_response(jsonify({'msg': 'Access Error - No Role Granted'})), 400

                user_perms = permission_repo.get_unpaginated(**{'role_id': user_role.role_id})

                perms = [perm.name for perm in user_perms]

                if len(perms) == 0:
                    return make_response(jsonify({'msg': 'Access Error - No Permission Granted'})), 400

                if permission not in perms:
                    return make_response(jsonify({'msg': 'Access Error - Permission Denied'})), 400

                return f(*args, **kwargs)
            return decorated
        return permission_checker
