from app.utils import db
from config import get_env
# from app import create_app
from app.utils.seed_data import seed_db
from app.utils.auth import Auth
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import app

# app = create_app(get_env('APP_ENV'))
migrate = Migrate(app, db)

manager = Manager(app)


manager.add_command('db', MigrateCommand)


@app.before_request
def check_token():
    return Auth.check_token()

@manager.command
def create_db():
    db.create_all()


@manager.command
def drop_db():
    db.drop_all()


@manager.command
def seed_all():
    seed_db()


@manager.command
def show_routes():
    from termcolor import colored

    count = 0
    for rule in app.url_map.iter_rules():
        methods = [m for m in rule.methods if m in ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']]
        line = 'Method: {method} | Route: {route} | Controller Endpoint: {endpoint}'.format(method=methods[0], route=rule, endpoint=rule.endpoint)

        if 'GET' in methods:
            print(colored(line, 'green'))

        if 'POST' in methods:
            print(colored(line, 'yellow'))

        if 'PUT' in methods or 'PATCH' in methods:
            print(colored(line, 'white'))

        if 'DELETE' in methods:
            print(colored(line, 'red'))

        count += 1
        
    print(count, ' Routes Found')

if __name__ == "__main__":
    manager.run()