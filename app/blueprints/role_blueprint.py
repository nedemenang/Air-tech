from app.blueprints.base_blueprint import Blueprint, BaseBlueprint, request, Security, Auth
from app.controllers.permission_controller import PermissionController

url_prefix = '{}/role'.format(BaseBlueprint.base_url_prefix)
role_blueprint = Blueprint('role', __name__, url_prefix=url_prefix)
permission_controller = PermissionController(request)

''' ROLES '''


@role_blueprint.route('/', strict_slashes=False, methods=['GET'])
@Auth.has_permission('read_roles')
def list_roles():
    return permission_controller.list_roles()


@role_blueprint.route('/<int:role_id>', strict_slashes=False, methods=['GET'])
@Auth.has_permission('read_roles')
def get_role(role_id):
    return permission_controller.get_role(role_id)


@role_blueprint.route('/', strict_slashes=False, methods=['POST'])
@Security.validator(['name|required'])
@Auth.has_permission('create_roles')
def create_role():
    return permission_controller.create_role()


@role_blueprint.route('/<int:role_id>', strict_slashes=False, methods=['PUT', 'PATCH'])
@Security.validator(['name|required'])
@Auth.has_permission('create_roles')
def update_role(role_id):
    return permission_controller.update_role(role_id)


@role_blueprint.route('/<int:role_id>', strict_slashes=False, methods=['GET'])
@Auth.has_permission('delete_roles')
def delete_role(role_id):
    return permission_controller.delete_role(role_id)