from app.repositories.base_repo import BaseRepo
from app.models.role import Role
from datetime import datetime


class RoleRepo(BaseRepo):

    def __init__(self):
        BaseRepo.__init__(self, Role)

    def create_role(self, name, help):
        role = Role(name=name, help=help)

        role.save()
        return role
