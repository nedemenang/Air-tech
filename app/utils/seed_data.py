from app.repositories.permission_repo import PermissionRepo
from app.repositories.role_repo import RoleRepo
from app.repositories.user_role_repo import UserRoleRepo
from app.repositories.user_repo import UserRepo
from datetime import datetime
from app.utils import db
from app.models.permission import Permission
from app.models.role import Role
from app.models.user_role import UserRole
from app.models.user import User
from sqlalchemy.exc import SQLAlchemyError
from app import bcrypt

user_data = [{'first_name': 'Nnamso', 'last_name': 'Johnson', 'middle_name': 'Hogan', 'email_address': 'nnamso.edemenang@gmail.com', 'password': bcrypt.generate_password_hash('Password1', 10).decode()}]

role_data = [{'id': '1', 'name': 'Administrator'}, {'id': '2', 'name': 'user'}]

user_role_data = [{'role_id': '1', 'user_id': 'nnamso.edemenang@gmail.com'}]

permission_data = [{'name': 'delete_airlines', 'role_id': '1', 'keyword': 'delete'},
                   {'name': 'create_airlines', 'role_id': '1', 'keyword': 'create'},
                   {'name': 'update_airlines', 'role_id': '1', 'keyword': 'update'},
                   # {'name': 'read_menu', 'role_id': '1', 'keyword': 'read'},
                   {'name': 'delete_flights', 'role_id': '1', 'keyword': 'delete'},
                   {'name': 'create_flights', 'role_id': '1', 'keyword': 'create'},
                   {'name': 'update_flights', 'role_id': '1', 'keyword': 'update'},
                   # {'name': 'read_meal_item', 'role_id': '1', 'keyword': 'read'},
                   {'name': 'delete_locations', 'role_id': '1', 'keyword': 'delete'},
                   {'name': 'create_locations', 'role_id': '1', 'keyword': 'create'},
                   {'name': 'update_locations', 'role_id': '1', 'keyword': 'update'},
                   # {'name': 'read_vendor', 'role_id': '1', 'keyword': 'read'},
                   {'name': 'delete_permissions', 'role_id': '1', 'keyword': 'delete'},
                   {'name': 'create_permissions', 'role_id': '1', 'keyword': 'create'},
                   {'name': 'update_permissions', 'role_id': '1', 'keyword': 'update'},
                   {'name': 'read_permissions', 'role_id': '1', 'keyword': 'read'},
                   {'name': 'delete_roles', 'role_id': '1', 'keyword': 'delete'},
                   {'name': 'create_roles', 'role_id': '1', 'keyword': 'create'},
                   {'name': 'update_roles', 'role_id': '1', 'keyword': 'update'},
                   {'name': 'read_roles', 'role_id': '1', 'keyword': 'read'},
                   {'name': 'delete_user_roles', 'role_id': '1', 'keyword': 'delete'},
                   {'name': 'create_user_roles', 'role_id': '1', 'keyword': 'create'},
                   {'name': 'update_user_roles', 'role_id': '1', 'keyword': 'update'},
                   {'name': 'read_user_roles', 'role_id': '1', 'keyword': 'read'}]

models = [User, Role, UserRole, Permission]

model_data = [user_data, role_data, user_role_data, permission_data]


def map_model_data():
    """it maps models and model_data"""
    model_data_map = []
    for index in range(0, len(models)):
        model_data_map.append({"model": models[index], 'data': model_data[index]})
    return model_data_map


def seed_db():
    errors = []
    mapped_model_data = map_model_data()
    for model_data in mapped_model_data:
        try:
            db.session.bulk_insert_mappings(
                model_data['model'], model_data['data'])
            db.session.commit()
        except SQLAlchemyError as error:
            errors.append({model_data['model'].__tablename__: error})
            db.session.rollback()
