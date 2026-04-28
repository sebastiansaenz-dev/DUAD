

from extensions import ma
from models import Roles

class RolesSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Roles
        load_instance = True

