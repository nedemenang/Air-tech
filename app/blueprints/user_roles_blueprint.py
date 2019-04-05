from app.blueprints.base_blueprint import Blueprint, BaseBlueprint, request, Security, Auth
from app.controllers.permission_controller import PermissionController

url_prefix = '{}/userRoles'.format(BaseBlueprint.base_url_prefix)
user_role_blueprint = Blueprint('user_roles', __name__, url_prefix=url_prefix)
permission_controller = PermissionController(request)

''' USER ROLES '''

@user_role_blueprint.route('/user/<string:user_id>', methods=['GET'])
def get_user_role(user_id):
    return permission_controller.get_user_role(user_id)


@user_role_blueprint.route('/user', methods=['POST'])
@Security.validator(['role_id|required:int', 'user_id|requied:int'])
def create_user_role():
    return permission_controller.create_user_role()


@user_role_blueprint.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user_role(user_id):
    return permission_controller.delete_user_role(user_id)