
from JWT_Manager import JWT_Manager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from sqlalchemy import MetaData

jwt_manager = JWT_Manager(private_path='./keys/private.pem', public_path='./keys/public.pem', algorithm='RS256')
migrate = Migrate()
metadata = MetaData(schema='lyfter_ecommerce')
db = SQLAlchemy(metadata=metadata)
ma = Marshmallow()
bcrypt = Bcrypt()