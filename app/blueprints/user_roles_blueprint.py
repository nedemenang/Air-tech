from app.blueprints.base_blueprint import Blueprint, BaseBlueprint, request, Security, Auth
from app.controllers.permission_controller import PermissionController

url_prefix = '{}/userRole'.format(BaseBlueprint.base_url_prefix)
user_role_blueprint = Blueprint('user_roles', __name__, url_prefix=url_prefix)
permission_controller = PermissionController(request)

''' USER ROLES '''

@user_role_blueprint.route('/<string:user_id>/', strict_slashes=False, methods=['GET'])
def get_user_role(user_id):
    return permission_controller.get_user_role(user_id)


@user_role_blueprint.route('/', strict_slashes=False, methods=['POST'])
@Security.validator(['roleId|required:int', 'userId|requied:int'])
def create_user_role():
    return permission_controller.create_user_role()


@user_role_blueprint.route('/<int:user_id>/', strict_slashes=False, methods=['DELETE'])
def delete_user_role(user_id):
    return permission_controller.delete_user_role(user_id)