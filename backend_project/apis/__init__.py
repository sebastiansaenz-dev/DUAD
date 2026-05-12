

from .products_api import products_bp
from .carts_api import carts_bp
from .orders_api import orders_bp
from .users_api import users_bp
from .refunds_api import refunds_bp
from .refresh_api import refresh_bp



def register_blueprints(app):
    app.register_blueprint(products_bp)
    app.register_blueprint(carts_bp)
    app.register_blueprint(orders_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(refunds_bp)
    app.register_blueprint(refresh_bp)





