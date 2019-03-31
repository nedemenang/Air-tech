from flask_api import FlaskAPI
from config import env, get_env
from flask_mail import Mail
from flask_bcrypt import Bcrypt
from app.utils import db
from app.blueprints.base_blueprint import BaseBlueprint
from celery import Celery
import celeryconflig

app = FlaskAPI(__name__, instance_relative_config=False)
app.config.from_object(env.app_env[get_env('APP_ENV')])
app.config.from_pyfile('../config/env.py')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# CORS(app)


def make_celery(app):
    # create context tasks in celery
    celery = Celery(
        app.import_name,
        broker=app.config['BROKER_URL']
    )
    celery.conf.update(app.config)
    celery.config_from_object(celeryconflig)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask

    return celery

celery = make_celery(app)

bcrypt = Bcrypt(app)
mail = Mail(app)


blueprint = BaseBlueprint(app)
blueprint.register()

db.init_app(app)

