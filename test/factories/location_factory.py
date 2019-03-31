import factory
from app.utils import db
from app.models.location import Location


class LocationFactory(factory.alchemy.SQLAlchemyModelFactory):

    class Meta:
        model = Location
        sqlalchemy_session = db.session

    id = factory.sequence(lambda n: n)
    location_code = 'ABV'
    location = 'Abuja'