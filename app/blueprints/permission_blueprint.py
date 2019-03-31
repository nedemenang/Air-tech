from app.blueprints.base_blueprint import Blueprint, BaseBlueprint, request, Security, Auth
from app.controllers.permission_controller import PermissionController

url_prefix = '{}/roles'.format(BaseBlueprint.base_url_prefix)
permission_blueprint = Blueprint('role', __name__, url_prefix=url_prefix)
permission_controller = PermissionController(request)

''' ROLES '''


@permission_blueprint.route('/', methods=['GET'])
@Auth.has_permission('view_roles')
def list_roles():
    return permission_controller.list_roles()


@permission_blueprint.route('/<int:role_id>', methods=['GET'])
@Auth.has_permission('view_roles')
def get_role(role_id):
    return permission_controller.get_role(role_id)


@permission_blueprint.route('/', methods=['POST'])
@Security.validator(['name|required'])
@Auth.has_permission('create_roles')
def create_role():
    return permission_controller.create_role()


@permission_blueprint.route('/<int:role_id>', methods=['PUT', 'PATCH'])
@Security.validator(['name|required'])
@Auth.has_permission('create_roles')
def update_role(role_id):
    return permission_controller.update_role(role_id)


@permission_blueprint.route('/<int:role_id>', methods=['GET'])
@Auth.has_permission('delete_roles')
def delete_role(role_id):
    return permission_controller.delete_role(role_id)


''' USER ROLES '''


@permission_blueprint.route('/user/<int:user_id>', methods=['GET'])
def get_user_role(user_id):
    return permission_controller.get_user_role(user_id)


@permission_blueprint.route('/user', methods=['POST'])
@Security.validator(['role_id|required:int', 'user_id|requied:int'])
def create_user_role():
    return permission_controller.create_user_role()


@permission_blueprint.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user_role(user_id):
    return permission_controller.delete_user_role(user_id)


''' ROLE PERMISSIONS '''


@permission_blueprint.route('/permissions/<int:role_id>', methods=['GET'])
def get_role_permissions(role_id):
    return permission_controller.get_role_permissions(role_id)


@permission_blueprint.route('/permissions', methods=['POST'])
@Security.validator(['role_id|required:int', 'name|required', 'keyword|required'])
def create_role_permission():
    return permission_controller.create_role_permission()


@permission_blueprint.route('/permissions/<int:permission_id>', methods=['DELETE'])
def delete_role_permission(permission_id):
    return permission_controller.delete_role_permission(permission_id)

