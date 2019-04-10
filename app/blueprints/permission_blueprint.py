from app.blueprints.base_blueprint import Blueprint, BaseBlueprint, request, Security, Auth
from app.controllers.permission_controller import PermissionController

url_prefix = '{}/permission'.format(BaseBlueprint.base_url_prefix)
permission_blueprint = Blueprint('permission', __name__, url_prefix=url_prefix)
permission_controller = PermissionController(request)

''' ROLE PERMISSIONS '''

@permission_blueprint.route('/permissions/<int:role_id>', strict_slashes=False, methods=['GET'])
def get_role_permissions(role_id):
    return permission_controller.get_role_permissions(role_id)


@permission_blueprint.route('/permissions', strict_slashes=False, methods=['POST'])
@Security.validator(['role_id|required:int', 'name|required', 'keyword|required'])
def create_role_permission():
    return permission_controller.create_role_permission()


@permission_blueprint.route('/remove/<int:permission_id>', strict_slashes=False, methods=['DELETE'])
def delete_role_permission(permission_id):
    return permission_controller.delete_role_permission(permission_id)
