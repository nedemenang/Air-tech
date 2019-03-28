from app.blueprints.base_blueprint import Blueprint, BaseBlueprint, request

url_prefix = '{}/'.format(BaseBlueprint.base_url_prefix)
sample_blueprint = Blueprint('sample', __name__, url_prefix=url_prefix)


@sample_blueprint.route('/', methods=['GET'])
def hello():
    return '''
                <h1>Hello! Welcome to AirTech</h2>
            '''
