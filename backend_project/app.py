
from flask import Flask
import os
from dotenv import load_dotenv

from apis import register_blueprints
from apis.admin_apis import register_admin_blueprints

from extensions import init_extensions

load_dotenv()

def create_app(config_override=None):
    
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

    app.config['REDIS_HOST'] = os.getenv("REDIS_HOST")
    app.config['REDIS_PORT'] = os.getenv("REDIS_PORT")
    app.config['REDIS_PASSWORD'] = os.getenv("REDIS_PASSWORD")

    if config_override:
        app.config.update(config_override)

    init_extensions(app)
    register_blueprints(app)
    register_admin_blueprints(app)

    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="localhost", port=5002, debug=True)




