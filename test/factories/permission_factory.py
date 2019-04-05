import factory
from app.utils import db
from app.models.role import Role
from app.models.permission import Permission
from app.models.user_role import UserRole


class RoleFactory(factory.alchemy.SQLAlchemyModelFactory):

    class Meta:
        model = Role
        sqlalchemy_session = db.session

    id = factory.sequence(lambda n: n+3)
    name = factory.Faker('word')
    help = 'A helping text'


class PermissionFactory(factory.alchemy.SQLAlchemyModelFactory):
    
    class Meta:
        model = Permission
        sqlalchemy_session = db.session

    id = factory.sequence(lambda n: n+1)
    name = factory.Faker('name')
    role_id = factory.SubFactory(RoleFactory)
    keyword = factory.Faker('word')


class UserRoleFactory(factory.alchemy.SQLAlchemyModelFactory):

    class Meta:
        model = UserRole
        sqlalchemy_session = db.session

    id = factory.Sequence(lambda n: n+2)
    role_id = factory.SubFactory(RoleFactory)
    user_id = factory.Sequence(lambda n: n)


