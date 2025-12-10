
from flask import Flask
from data import check_if_file_exist
from users_authentication import register_api as register_users
from products import register_api as register_products
from carts import register_api as register_carts
from sales import register_api as register_sales
from receipts import register_api as register_receipts
from refunds import register_api as register_refunds

app = Flask(__name__)

register_users(app)
register_products(app)
register_carts(app)
register_sales(app)
register_receipts(app)
register_refunds(app)

if __name__ == "__main__":
    check_if_file_exist("./users.json")
    check_if_file_exist("./products.json")
    check_if_file_exist('./carts.json')
    check_if_file_exist('./sales.json')
    check_if_file_exist('./receipts.json')
    check_if_file_exist('./refunds.json')
    app.run(host="localhost", port=5002, debug=True)




