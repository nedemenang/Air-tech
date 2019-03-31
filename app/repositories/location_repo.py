from app.repositories.base_repo import BaseRepo
from app.models.location import Location
from datetime import datetime


class LocationRepo(BaseRepo):

    def __init__(self):
        BaseRepo.__init__(self, Location)

    def create_location(self, location_code, location):
        location = Location(location_code=location_code, location=location)

        location.save()
        return location
