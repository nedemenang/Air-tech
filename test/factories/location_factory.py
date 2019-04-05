import factory
from app.utils import db
from app.models.location import Location
import string
import random


class LocationFactory(factory.alchemy.SQLAlchemyModelFactory):

    class Meta:
        model = Location
        sqlalchemy_session = db.session

    id = factory.sequence(lambda n: n)
    location_code = ''.join(random.choices(string.ascii_uppercase, k=3))
    location = factory.Faker('country')