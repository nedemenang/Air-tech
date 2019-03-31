from flask import Blueprint, request
from app.utils.security import Security
from app.utils.auth import Auth


class BaseBlueprint:
    base_url_prefix = '/api/v1'

    def __init__(self, app):
        self.app = app

    def register(self):

        '''Register all App blueprints here '''
        from app.blueprints.sample_blueprint import sample_blueprint
        from app.blueprints.user_blueprint import user_blueprint
        from app.blueprints.card_blueprint import card_blueprint
        from app.blueprints.flight_blueprint import flight_blueprint
        from app.blueprints.location_blueprint import location_blueprint
        from app.blueprints.permission_blueprint import permission_blueprint
        from app.blueprints.ticket_blueprint import ticket_blueprint

        self.app.register_blueprint(sample_blueprint)
        self.app.register_blueprint(user_blueprint)
        self.app.register_blueprint(card_blueprint)
        self.app.register_blueprint(flight_blueprint)
        self.app.register_blueprint(location_blueprint)
        self.app.register_blueprint(permission_blueprint)
        self.app.register_blueprint(ticket_blueprint)
