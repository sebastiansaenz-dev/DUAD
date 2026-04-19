
from flask import Flask
import os
from dotenv import load_dotenv
from extensions import ma, db, migrate, bcrypt
from apis.users_api import register_api as register_users
from apis.products_api import register_api as register_products
from apis.carts_api import register_api as register_carts
from apis.orders_api import register_api as register_orders
from apis.refunds_api import register_api as register_refunds


from apis.admin_apis.admin_users_api import register_api as register_admin_users
from apis.admin_apis.admin_carts_api import register_api as register_admin_carts
from apis.admin_apis.admin_orders_api import register_api as register_admin_orders
from apis.admin_apis.admin_products_api import register_api as register_admin_products
from apis.admin_apis.admin_refunds_api import register_api as register_admin_refunds
# from models import ProductsCarts, ProductsOrders, UsersRoles, Users, Carts, CartsStatus, Orders, OrdersStatus, PaymentMethods, Products, Roles

load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

db.init_app(app)
migrate.init_app(app, db)
ma.init_app(app)
bcrypt.init_app(app)


register_users(app)
register_products(app)
register_carts(app)
register_orders(app)
register_refunds(app)

register_admin_users(app)
register_admin_carts(app)
register_admin_orders(app)
register_admin_products(app)
register_admin_refunds(app)


if __name__ == "__main__":
    app.run(host="localhost", port=5002, debug=True)




