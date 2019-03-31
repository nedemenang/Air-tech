from app.blueprints.base_blueprint import Blueprint, BaseBlueprint, Security, request, Auth
from app.controllers.flight_seats_controller import FlightSeatController


url_prefix = '{}/flightSeat'.format(BaseBlueprint.base_url_prefix)
flight_seat_blueprint = Blueprint('flight_seat', __name__, url_prefix=url_prefix)
flight_seat_controller = FlightSeatController(request)


@flight_seat_blueprint.route('/<int:flight_id>/', methods=['GET'])
def list_flight_seats(flight_id):
    return flight_seat_controller.get_all_seats_on_flight(flight_id)


@flight_seat_blueprint.route('/available/<int:flight_id>/', methods=['GET'])
def get_available_seats_on_flight(flight_id):
    return flight_seat_controller.get_available_seats_on_flight(flight_id)


@flight_seat_blueprint.route('/unavailable/<int:flight_id>', methods=['GET'])
def get_unavailable_seats_on_flight(flight_id):
    return flight_seat_controller.get_unavailable_seats_on_flight(flight_id)