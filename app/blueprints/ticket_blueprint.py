from app.blueprints.base_blueprint import Blueprint, BaseBlueprint, Security, request, Auth
from app.controllers.ticket_controller import TicketController


url_prefix = '{}/ticket'.format(BaseBlueprint.base_url_prefix)
ticket_blueprint = Blueprint('ticket', __name__, url_prefix=url_prefix)
ticket_controller = TicketController(request)


@ticket_blueprint.route('/', methods=['GET'])
def list_ticket():
    return ticket_controller.get_tickets()


@ticket_blueprint.route('/<int:ticket_id>/', methods=['GET'])
def get_ticket(ticket_id):
    return ticket_controller.get_ticket(ticket_id)


@ticket_blueprint.route('/', methods=['POST'])
@Security.validator(['flightSeatId|required:int', 'status|required:string', 'userId|required:int'])
def create_ticket():
    return ticket_controller.create_ticket()


@ticket_blueprint.route('/<int:ticket_id>/', methods=['PUT'])
@Security.validator(['flightSeatId|required:int', 'status|required:string', 'userId|required:int'])
def update_ticket(ticket_id):
    return ticket_controller.update_ticket(ticket_id)


@ticket_blueprint.route('/<int:ticket_id>/', methods=['DELETE'])
def delete_ticket(ticket_id):
    return ticket_controller.delete_ticket(ticket_id)
