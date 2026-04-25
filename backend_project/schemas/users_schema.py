

from models import Users
from extensions import ma
from marshmallow import fields, validate



class UsersSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Users
        load_instance = True

    id = ma.auto_field(dump_only=True)
    email = fields.Email(required=True, error_messages={'Invalid': 'Not a valid email address'})
    password = fields.Str(required=True, load_only=True, validate=[validate.Length(min=8)])
    created_at = ma.auto_field(load_only=True)

    roles = ma.Nested('RolesSchema', many=True)
    

from .roles_schema import RolesSchema

