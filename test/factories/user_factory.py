import factory
from app.utils import db
from app.models.user import User
import string
import random


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):

    class Meta:
        model = User
        sqlalchemy_session = db.session

    id = factory.sequence(lambda n: n+2)
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    middle_name = factory.Faker('first_name')
    photo_link = factory.Faker('image_url')
    email_address = factory.Faker('email')
    password = '$2b$10$6YvMfXFD/Yx1YYnbnYbdLu0M.L/BeepQ/UuM1ddM3wiQPGYLjbXNy'