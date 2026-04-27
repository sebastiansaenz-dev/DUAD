


from .admin_carts_api import admin_carts_bp
from .admin_orders_api import admin_orders_bp
from .admin_products_api import admin_products_bp
from .admin_refunds_api import admin_refunds_bp
from .admin_users_api import admin_users_bp



def register_admin_blueprints(app):
    app.register_blueprint(admin_carts_bp)
    app.register_blueprint(admin_orders_bp)
    app.register_blueprint(admin_products_bp)
    app.register_blueprint(admin_refunds_bp)
    app.register_blueprint(admin_users_bp)




