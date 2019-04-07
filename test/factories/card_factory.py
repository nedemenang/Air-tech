import factory
from app.utils import db
from app.models.card_detail import CardDetail
import string
import random
from datetime import datetime, timedelta
from json import dumps
from .user_factory import UserFactory


class CardFactory(factory.alchemy.SQLAlchemyModelFactory):

    class Meta:
        model = CardDetail
        sqlalchemy_session = db.session

    id = factory.sequence(lambda n: n)
    card_number = ''.join(random.choices(string.digits, k=16))
    expiry_month = 1
    expiry_year = 25
    securiy_number = ''.join(random.choices(string.digits, k=3))
    user_id = factory.SubFactory(UserFactory)