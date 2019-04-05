'''
    A controller module for user-related
'''
import os
import re
from datetime import datetime
from app.blueprints.base_blueprint import Auth
from app.controllers.base_controller import BaseController
from app.repositories.user_repo import UserRepo
from werkzeug.utils import secure_filename
from flask import url_for
from app import bcrypt

UPLOAD_FOLDER = './app/uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


class UserController(BaseController):
    def __init__(self, request):
        BaseController.__init__(self, request)
        self.user_repo = UserRepo()

    def get_user(self, email_address):
        user = self.user_repo.get(email_address)
        if user:
            user = user.serialize()
            return self.handle_response('OK', payload={'user': user})
        else:
            return self.handle_response('Bad Request - Invalid or missing email address', status_code=400)

    def create_user(self):
        first_name, last_name, middle_name, email_address, password = self.request_params('firstName', 'lastName', 'middleName', 'emailAddress', 'password')
        user = self.user_repo.filter_first(**{'email_address': email_address})
        if user:
            return self.handle_response('Bad Request - email address already exists', status_code=400)

        if not re.fullmatch(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email_address):
            return self.handle_response('Bad Request - enter valid email address', status_code=400)

        if not re.fullmatch(r"(?=^.{8,}$)(?=.*\d)(?=.*[!@#$%^&*]+)(?![.\n])(?=.*[A-Z])(?=.*[a-z]).*$", password):
            return self.handle_response('Bad Request - password not strong enough', status_code=400)

        password = bcrypt.generate_password_hash(password, 10).decode()
        user = self.user_repo.create_user(first_name, last_name, middle_name, email_address, password)
        return self.handle_response('OK', payload={'user': user.serialize()}, status_code=201)

    def login(self):
        email_address, password = self.request_params('emailAddress', 'password')
        user = self.user_repo.filter_first(**{'email_address': email_address})
        if user:
            if bcrypt.check_password_hash(user.password, password):
                token = Auth.create_token(user.email_address)
                del user.password
                return self.handle_response('OK', payload={'user': user.serialize(), 'token': token.decode()})
            else:
                return self.handle_response('Bad Request - authentication error', status_code=400)
        else:
            return self.handle_response('Bad Request - authentication error', status_code=400)

    def allowed_file(self, filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    def upload_picture(self):
        email_address = self.request.form.get('emailAddress')
        if email_address:
            user = self.user_repo.filter_first(**{'email_address': email_address})
            if 'file' not in self.request.files:
                return self.handle_response('File not included', status_code=400)
            file = self.request.files['file']
            if file.filename == '':
                return self.handle_response('File not selected', status_code=400)
            if file and self.allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(UPLOAD_FOLDER, filename))
                updates = {}
                updates['photo_link'] = os.path.join(UPLOAD_FOLDER, filename)
                self.user_repo.update(user, **updates)
                return self.handle_response('OK')
            return self.handle_response('Invalid file type', status_code=400)
        return self.handle_response('Bad Request - user Id not included', status_code=400)

    def reset_password(self):
        email_address, password = self.request_params('emailAddress', 'password')
        user = self.user_repo.filter_first(**{'email_address': email_address})
        if user:
            if not re.fullmatch(r"(?=^.{8,}$)(?=.*\d)(?=.*[!@#$%^&*]+)(?![.\n])(?=.*[A-Z])(?=.*[a-z]).*$", password):
                return self.handle_response('Bad Request - password not strong enough', status_code=400)

            password = bcrypt.generate_password_hash(password, 10).decode()

            updates = {'password': password}
            self.user_repo.update(user, **updates)
            return self.handle_response('OK', payload={'user': user.serialize()})
        else:
            return self.handle_response('Bad Request - authentication error', status_code=400)
