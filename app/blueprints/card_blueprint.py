from app.blueprints.base_blueprint import Blueprint, BaseBlueprint, Security, request, Auth
from app.controllers.card_controller import CardDetailController


url_prefix = '{}/card'.format(BaseBlueprint.base_url_prefix)
card_blueprint = Blueprint('card', __name__, url_prefix=url_prefix)
card_controller = CardDetailController(request)


@card_blueprint.route('/', methods=['GET'])
def list_card_details():
    return card_controller.list_card_details()


@card_blueprint.route('/<int:card_id>/', methods=['GET'])
def get_card_details(card_id):
    return card_controller.get_card_details(card_id)


@card_blueprint.route('/', methods=['POST'])
@Security.validator(['cardNumber|required:string', 'expiryMonth|required:int', 'expiryYear|required:int', 'securityNumber|required:int', 'userId|required:int'])
def create_card_details():
    return card_controller.create_card_details()


@card_blueprint.route('/<int:card_id>/', methods=['PATCH', 'PUT'])
@Security.validator(['cardNumber|required:string', 'expiryMonth|required:int', 'expiryYear|required:int', 'securityNumber|required:int', 'userId|required:int'])
def update_card_details(card_id):
    return card_controller.update_card_details(card_id)


@card_blueprint.route('/<int:card_id>/', methods=['DELETE'])
def delete_card_detail(card_id):
    return card_controller.delete_card_detail(card_id)
