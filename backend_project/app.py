
from flask import Flask
import os
from dotenv import load_dotenv
from datetime import timedelta
from sqlalchemy import select
from models import TokenBlocklist


from apis import register_blueprints
from apis.admin_apis import register_admin_blueprints

from extensions import init_extensions, jwt_manager, db

load_dotenv()

def create_app(config_override=None):
    
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

    app.config['REDIS_HOST'] = os.getenv("REDIS_HOST")
    app.config['REDIS_PORT'] = os.getenv("REDIS_PORT")
    app.config['REDIS_PASSWORD'] = os.getenv("REDIS_PASSWORD")

    app.config['JWT_ALGORITHM'] = 'RS256'
    app.config['JWT_PRIVATE_KEY'] = open('./keys/private_key.pem').read()
    app.config['JWT_PUBLIC_KEY'] = open('./keys/public_key.pem').read()

    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=15)
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=7)

    if config_override:
        app.config.update(config_override)

    init_extensions(app)
    register_blueprints(app)
    register_admin_blueprints(app)

    @jwt_manager.token_in_blocklist_loader
    def check_if_token_revoke(jwt_header, jwt_payload):
        jti = jwt_payload['jti']

        stmt = select(TokenBlocklist).where(TokenBlocklist.jti == jti)

        token = db.session.execute(stmt).first()

        return token is not None
    
    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="localhost", port=5002, debug=True)




