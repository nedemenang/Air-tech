from app.repositories.base_repo import BaseRepo
from app.models.permission import Permission
from datetime import datetime


class PermissionRepo(BaseRepo):

    def __init__(self):
        BaseRepo.__init__(self, Permission)

    def create_permission(self, role_id, name, keyword):
        permission = Permission(role_id=role_id, name=name, keyword=keyword)

        permission.save()
        return permission
