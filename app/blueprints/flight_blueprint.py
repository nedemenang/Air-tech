from app.blueprints.base_blueprint import Blueprint, BaseBlueprint, Security, request, Auth
from app.controllers.flight_controller import FlightController


url_prefix = '{}/flight'.format(BaseBlueprint.base_url_prefix)
flight_blueprint = Blueprint('flight', __name__, url_prefix=url_prefix)
flight_controller = FlightController(request)


@flight_blueprint.route('/', methods=['GET'])
def list_flight():
    return flight_controller.get_flights()


@flight_blueprint.route('/<int:flight_id>/', methods=['GET'])
def get_flight(flight_id):
    return flight_controller.get_flight(flight_id)


@flight_blueprint.route('/available/<int:flight_id>', methods=['GET'])
def get_available_seats(flight_id):
    return flight_controller.get_available_seats(flight_id)


@flight_blueprint.route('/reserved/<int:flight_id>', methods=['GET'])
def get_users_booked_on_flight(flight_id):
    return flight_controller.get_users_booked_on_flight(flight_id)


@flight_blueprint.route('/<string:from_location>/<string:to_location>/<string:departure_date>/', methods=['GET'])
def get_flights_by_location_and_date(from_location, to_location, departure_date):
    return flight_controller.get_flights_by_location_and_date(from_location, to_location, departure_date)


@flight_blueprint.route('/<string:from_location>/<string:to_location>/', methods=['GET'])
def get_flights_by_location(from_location, to_location):
    return flight_controller.get_flights_by_location(from_location, to_location)


@flight_blueprint.route('/', methods=['POST'])
@Auth.has_permission('create_flights')
@Security.validator(['flightCode|required:string', 'fromLocation|required:string', 'status|required:string', 'toLocation|required:string', 'depatureTime|required:string', 'arrivalTime|required:string', 'noOfSeats|required:int'])
def create_flight():
    return flight_controller.create_flight()


@flight_blueprint.route('/<int:flight_id>/', methods=['PUT', 'PATCH'])
@Security.validator(['flightCode|required:string', 'fromLocation|required:string', 'status|required:string', 'toLocation|required:string', 'depatureTime|required:string', 'arrivalTime|required:string', 'noOfSeats|required:int'])
@Auth.has_permission('update_flights')
def update_flight(flight_id):
    return flight_controller.update_flight(flight_id)


@flight_blueprint.route('/<int:flight_id>/', methods=['DELETE'])
@Auth.has_permission('delete_flights')
def delete_flight(flight_id):
    return flight_controller.delete_flight(flight_id)
