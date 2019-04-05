import factory
from app.utils import db
from app.models.ticket import Ticket
from .flight_factory import FlightFactory
from .user_factory import UserFactory
from .flight_seat_factory import FlightSeatFactory
import random
import string


class TicketFactory(factory.alchemy.SQLAlchemyModelFactory):

    class Meta:
        model = Ticket
        sqlalchemy_session = db.session

    id = factory.sequence(lambda n: n)
    ticket_no = ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
    status = "Booked"
    user_id = factory.SubFactory(UserFactory)
    flight_seat_id = factory.SubFactory(FlightSeatFactory)
