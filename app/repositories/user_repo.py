from app.repositories.base_repo import BaseRepo
from app.models.user import User
from datetime import datetime


class UserRepo(BaseRepo):

    def __init__(self):
        BaseRepo.__init__(self, User)

    def create_user(self, first_name, last_name, middle_name, email_address, password):
        user = User(first_name=first_name, last_name=last_name, middle_name=middle_name, email_address=email_address, password=password)

        user.save()
        return user
