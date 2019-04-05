import factory
from app.utils import db
from .flight_factory import FlightFactory
from app.models.flight_seats import FlightSeat
import string
import random


class FlightSeatFactory(factory.alchemy.SQLAlchemyModelFactory):
    
    class Meta:
        model = FlightSeat
        sqlalchemy_session = db.session

    id = factory.sequence(lambda n: n)
    seat_number = ''.join(random.choices(string.ascii_uppercase + string.digits, k=2))
    is_available = True
    flight_id = factory.SubFactory(FlightFactory)
