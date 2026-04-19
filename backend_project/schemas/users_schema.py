

from models import Users
from extensions import ma



class UsersSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Users
        load_instance = True

    id = ma.auto_field(dump_only=True)
    created_at = ma.auto_field(load_only=True)
    password = ma.auto_field(load_only=True)

    roles = ma.Nested('RolesSchema', many=True)
    

from .roles_schema import RolesSchema

