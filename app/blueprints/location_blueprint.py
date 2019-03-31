from app.blueprints.base_blueprint import Blueprint, BaseBlueprint, Security, request, Auth
from app.controllers.location_controller import LocationController


url_prefix = '{}/location'.format(BaseBlueprint.base_url_prefix)
location_blueprint = Blueprint('location', __name__, url_prefix=url_prefix)
location_controller = LocationController(request)


@location_blueprint.route('/', methods=['GET'])
def list_locations():
    return location_controller.get_locations()


@location_blueprint.route('/<int:location_id>/', methods=['GET'])
def get_location(location_id):
    return location_controller.get_location(location_id)


@location_blueprint.route('/', methods=['POST'])
@Security.validator(['locationCode|required:string', 'location|required:string'])
@Auth.has_permission('create_locations')
def create_location():
    return location_controller.create_location()


@location_blueprint.route('/<int:location_id>/', methods=['POST'])
@Security.validator(['locationCode|required:string', 'location|required:string'])
@Auth.has_permission('update_locations')
def update_location(location_id):
    return location_controller.update_location(location_id)


@location_blueprint.route('/<int:location_id>/', methods=['DELETE'])
@Auth.has_permission('delete_locations')
def delete_location(location_id):
    return location_controller.delete_location(location_id)
