from app.blueprints.base_blueprint import Blueprint, BaseBlueprint, Security, request, Auth
from app.controllers.user_controller import UserController


url_prefix = '{}/user'.format(BaseBlueprint.base_url_prefix)
user_blueprint = Blueprint('user', __name__, url_prefix=url_prefix)
user_controller = UserController(request)


@user_blueprint.route('/', methods=['POST'])
@Security.validator(['firstName|required:string', 'lastName|required:string', 'emailAddress|required:string', 'password|required:string'])
def create_user():
    return user_controller.create_user()


@user_blueprint.route('/upload', methods=['POST'])
def upload_picture():
    return user_controller.upload_picture()


@user_blueprint.route('/login', methods=['POST'])
@Security.validator(['emailAddress|required:string', 'password|required:string'])
def login():
    return user_controller.login()


@user_blueprint.route('/reset', methods=['PUT'])
@Security.validator(['emailAddress|required:string', 'password|required:string'])
def reset_password(user_id):
    return user_controller.reset_password()
