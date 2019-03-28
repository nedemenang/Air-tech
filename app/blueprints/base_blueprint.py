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
        
        self.app.register_blueprint(sample_blueprint)
        
