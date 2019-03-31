'''A controller module for flight-related
'''
from datetime import datetime
from app.controllers.base_controller import BaseController
from app.repositories.location_repo import LocationRepo


class LocationController(BaseController):
    def __init__(self, request):
        BaseController.__init__(self, request)
        self.location_repo = LocationRepo()

    def get_locations(self):
        locations = self.location_repo.filter_by(**{'is_deleted': 'false'})
        location_list = [location.serialize() for location in locations.items]
        return self.handle_response('OK', payload={'locations': location_list, 'meta': self.pagination_meta(locations)})

    def get_location(self, location_id):
        location = self.location_repo.get(location_id)
        if location:
            location = location.serialize()
            return self.handle_response('OK', payload={'location': location})
        else:
            return self.handle_response('Bad Request - Invalid or missing location_id', status_code=400)

    def create_location(self):
        location_code, location_name = self.request_params('locationCode', 'location')
        location = self.location_repo.create_location(location_code, location_name)
        return self.handle_response('OK', payload={'location': location.serialize()}, status_code=201)
  
    def update_location(self, location_id):
        location_code, location_name = self.request_params('locationCode', 'location')

        location = self.location_repo.get(location_id)
        if location:
            updates = {}
            if location_code:
                updates['location_code'] = location_code
            if location_name:
                updates['location'] = location_name
            
            self.location_repo.update(location, **updates)
            return self.handle_response('OK', payload={'location': location.serialize()})
        return self.handle_response('Invalid or incorrect location_id provided', status_code=400)

    def delete_location(self, location_id):
        location = self.location_repo.get(location_id)
        updates = {}
        if location:
            updates['is_deleted'] = True

            self.location_repo.update(location, **updates)
            return self.handle_response('OK', payload={"status": "success"})
        return self.handle_response('Invalid or incorrect location_id provided', status_code=400)

