import factory
from app.utils import db
from app.models.flight import Flight
import string
import random
from datetime import datetime, timedelta
from json import dumps


class FlightFactory(factory.alchemy.SQLAlchemyModelFactory):

    class Meta:
        model = Flight
        sqlalchemy_session = db.session

    id = factory.sequence(lambda n: n)
    flight_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    status = 'OnTime'
    from_location = ''.join(random.choices(string.ascii_uppercase, k=3))
    to_location = ''.join(random.choices(string.ascii_uppercase, k=3))
    departure_time = datetime.now()
    arrival_time = datetime.now() + timedelta(hours=2)
    price = 25000.00
    departure_date = datetime.date(departure_time)
    no_of_seats = 150
