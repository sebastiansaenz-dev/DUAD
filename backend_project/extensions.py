
from JWT_Manager import JWT_Manager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from sqlalchemy import MetaData
from cache import CacheManager

jwt_manager = JWT_Manager(private_path='./keys/private.pem', public_path='./keys/public.pem', algorithm='RS256')
migrate = Migrate()
metadata = MetaData(schema='lyfter_ecommerce')
db = SQLAlchemy(metadata=metadata)
ma = Marshmallow()
bcrypt = Bcrypt()
cache_manager = CacheManager()

def init_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    bcrypt.init_app(app)
    cache_manager.init_app(app, decode_responses=True)