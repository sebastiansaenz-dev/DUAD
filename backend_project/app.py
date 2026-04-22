
from flask import Flask
import os
from dotenv import load_dotenv

from apis import register_blueprints
from apis.admin_apis import register_admin_blueprints

from extensions import ma, db, migrate, bcrypt

load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

db.init_app(app)
migrate.init_app(app, db)
ma.init_app(app)
bcrypt.init_app(app)

register_blueprints(app)
register_admin_blueprints(app)


if __name__ == "__main__":
    app.run(host="localhost", port=5002, debug=True)




