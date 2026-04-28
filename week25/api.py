from db import DB_Manager
from JWT_Manager import JWT_Manager
from flask import Flask, request, Response, jsonify
from models import Base
from functools import wraps
from cache import CacheManager
from dotenv import load_dotenv
import os
import redis
import json

load_dotenv()

app = Flask("user-service")
db_manager = DB_Manager()
jwt_manager = JWT_Manager(private_path='./private_key.pem', public_path='./public_key.pem', algorithm='RS256')
cache_manager = CacheManager(
    host=os.getenv("REDIS_HOST"),
    port=int(os.getenv("REDIS_PORT")),
    password=os.getenv("REDIS_PASSWORD")
)
Base.metadata.create_all(db_manager.engine)


def require_admin(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token or not token.startswith("Bearer "):
            return jsonify('invalid token'), 400

        token = token.replace("Bearer ", "")

        decoded = jwt_manager.decode(token)

        if decoded is None:
            return jsonify('Invalid token'), 400
        
        user_role = decoded.get('role')

        if user_role != 'admin':
            return jsonify('invalid permissions'), 403

        return func(*args, **kwargs)
    return wrapper

def require_auth(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token or not token.startswith("Bearer "):
            return jsonify('invalid token'), 400
        
        token = token.replace("Bearer ", "")

        decoded = jwt_manager.decode(token)

        if decoded is None:
            return jsonify('invalid token'), 403
        
        user_id = decoded.get('id')

        kwargs['current_user_id'] = user_id

        return func(*args, **kwargs)
    return wrapper


@app.route("/liveness")
def liveness():
    return "<p>Hello, World!</p>"


##################################################
# CRUD users

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()  # data is empty
    if(data.get('username') == None or data.get('password') == None):
        return Response(status=400)
    else:
        user_data = {
            "username": data.get('username'),
            "password": data.get('password')
        }
        new_user = db_manager.users.create(user_data)

        payload = {
            'id': new_user.id,
            'role': new_user.roles.name
        }

        token = jwt_manager.encode(payload)
        
        return jsonify(token=token)

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()  # data is empty
    if(data.get('username') == None or data.get('password') == None):
        return Response(status=400)
    else:
        user_data = {
            "username": data.get('username'),
            "password": data.get('password')
        }

        result = db_manager.users.get_all(user_data)

        if not result:
            return Response(status=403)

        user = result[0]
    
        payload = {
            'id': user.id,
            'role': user.roles.name
        }

        token = jwt_manager.encode(payload)
    
        return jsonify(token=token)

@app.route('/me')
@require_auth
def me(current_user_id):
    try:

        user = db_manager.users.get_by_id(current_user_id)

        return jsonify(id=current_user_id, username=user.username)

    except Exception as e:
        return Response(status=500)

@app.route('/users')
@require_admin
def get_users():

    filters = request.args.to_dict()
    users = db_manager.users.get_all(filters, load_role=True)

    return jsonify({
        "id": u.id,
        "username": u.username,
        "role": u.role.name
    } for u in users)


@app.route('/users/<id>', methods=['PATCH'])
@require_admin
def admin_update_user(id):
    try:
        new_data = request.get_json()

        db_manager.users.update(new_data, {"id": id})

        user = db_manager.users.get_by_id(id, load_role=True)

        return jsonify({
            "id": user.id,
            "username": user.username,
            "role": user.roles.name
        })
    
    except Exception as ex:
        print(ex)
        return jsonify('there was an error')


@app.route('/users/<id>', methods=['DELETE'])
@require_admin
def admin_delete_user(id):
    try:
        db_manager.users.delete({"id": id})

        return jsonify('user deleted')

    except LookupError as ex:
        print(ex)
    
    except Exception as ex:
        print(ex)
        return jsonify('there was an error'), 500
    

@app.route('/users', methods=['PATCH'])
@require_auth
def update_user(current_user_id):
    try:
        new_data = request.get_json()

        db_manager.users.update(new_data, {"id": current_user_id})

        user = db_manager.users.get_by_id(current_user_id, load_role=True)

        return jsonify({
            "id": user.id,
            "username": user.username,
            "role": user.roles.name
        })

        return jsonify(db_manager.users.to_dict(user))

    except Exception as ex:
        print(ex)
        return Response(status=500)


@app.route('/users', methods=['DELETE'])
@require_auth
def delete_user(current_user_id):
    try:
        db_manager.users.delete({"id": current_user_id})
        return jsonify('user deleted')
    
    except LookupError as ex:
        print(ex)

    except Exception as ex:
        print(ex)
        return Response(500)
    



########################################
# CRUD FRUITS

@app.route('/fruits')
def get_fruits():
    try:
        filters = request.args.to_dict()

        cache_key = f"fruits:all:{filters}" if filters else "fruits:all"


        cached_fruits = cache_manager.get_data(cache_key)
        if cached_fruits:
            return jsonify(json.loads(cached_fruits))

        fruits = db_manager.fruits.get_all(filters)

        fruits_string = json.dumps([db_manager.fruits.to_dict(f) for f in fruits])

        fruits_dict = [db_manager.fruits.to_dict(f) for f in fruits]

        if cache_key == "fruits:all":
            cache_manager.store_data(cache_key, fruits_string, time_to_live=600)

        cache_manager.store_data(cache_key, fruits_string, time_to_live=300)

        return jsonify(fruits_dict)
    
    except Exception as ex:
        print(ex)
        return jsonify('there was as error')


@app.route('/fruits/<id>', methods=['GET'])
def get_fruits_by_id(id):
    try:

        cache_fruit = cache_manager.get_data(f'fruits:{id}')

        if cache_fruit:
            return jsonify(json.loads(cache_fruit))

        fruit = db_manager.fruits.get_by_id(id)

        if not fruit:
            return jsonify(message='fruit not found'), 404

        fruit_dict = db_manager.fruits.to_dict(fruit)

        fruit_string = json.dumps(fruit_dict)

        cache_manager.store_data(f'fruits:{id}', fruit_string, time_to_live=3600)

        return jsonify(fruit_dict)

    
    except Exception as ex:
        print(ex)
        return jsonify('there was as error')


@app.route('/fruits', methods=['POST'])
@require_admin
def create_fruit():
    try:
        data = request.get_json()
        if data.get('name') == None or data.get('price') == None or data.get('quantity') == None:
            return Response(status=400)

        fruit_data = {
            "name": data.get('name'),
            "price": data.get('price'),
            "quantity": data.get('quantity')
        }

        new_fruit = db_manager.fruits.create(fruit_data)
        new_fruit_dict = db_manager.fruits.to_dict(new_fruit)

        cache_manager.store_data(f'fruits:{new_fruit.id}', json.dumps(new_fruit_dict), time_to_live=3600)
        cache_manager.delete_data('fruits:all')

        return jsonify(new_fruit_dict)

    except Exception as ex:
        print(ex)
        return jsonify("there was an error"), 500
    

@app.route('/fruits/<id>', methods=['PATCH'])
@require_admin
def update_fruit(id):
    try:
        new_data = request.get_json()

        update_fruit = db_manager.fruits.update(new_data, {"id": id})

        if not update_fruit:
            return jsonify(message='fruit not found'), 404

        if update_fruit:
            for fruit in update_fruit:
                cache_manager.delete_data(f'fruits:{fruit.id}')

        cache_manager.delete_data('fruits:all')

        return jsonify([db_manager.fruits.to_dict(f) for f in update_fruit])
    except Exception as ex:
        print(ex)
        return jsonify('there was an error'), 500


@app.route('/fruits/<id>', methods=['DELETE'])
@require_admin
def delete_fruit(id):
    try:

        db_manager.fruits.delete({"id": id})
        cache_manager.delete_data(f'fruits:{id}')
        cache_manager.delete_data('fruits:all')

        return jsonify('item deleted')

    except LookupError as ex:
        print(ex)

    except Exception as ex:
        print(ex)
        return Response(status=500)
    
################################

@app.route('/buy', methods=['POST'])
@require_auth
def buy(current_user_id):
    try:
        items = request.get_json()
        total = 0
        valid_items = []

        for item in items:

            check_fruit = db_manager.fruits.get_by_id(item["id"])

            if check_fruit == None:
                return jsonify('fruit not found'), 404

            if "id" not in item and "quantity" not in item:
                return jsonify('items must have id and quantity'), 400
            
            if item['quantity'] > check_fruit.quantity and item['quantity'] > 0:
                return jsonify('insufficient stock'), 400
            
            total += (check_fruit.price * item['quantity'])

            valid_items.append({
                "fruit": check_fruit,
                "quantity": item['quantity']
            })
            

        new_receipt = db_manager.receipts.create({"user_id": current_user_id, "total": total})

        for item in valid_items:

            receipt_fruits_data = {
                'fruit_id': item['fruit'].id,
                'receipt_id': new_receipt.id,
                'quantity': item['quantity']
            }
            db_manager.receipts_fruits.create(receipt_fruits_data)


            db_manager.fruits.update({'quantity': item['fruit'].quantity - item['quantity']}, {'id': item['fruit'].id})

            cache_manager.delete_data(f'fruits:{item['fruit'].id}')
        cache_manager.delete_data('fruits:all')
        return jsonify({
            'message': 'purchase successful',
            'receipt_id': new_receipt.id
        })

    except Exception as ex:
        print(ex)
        return Response(status=500)

        

################################

@app.route('/receipts')
@require_auth
def get_receipts(current_user_id):
    try:

        receipts = db_manager.receipts.get_all({'user_id': current_user_id}, load_user=True, load_fruits=True)

        result = []


        for r in receipts:
            fruits_data = []
            for rf in r.receipts_fruits:

                fruits_data.append({
                    "id": rf.fruit.id,
                    "name": rf.fruit.name,
                    "price": rf.fruit.price,
                    "quantity": rf.quantity
                })

            result.append({
                "id": r.id,
                "date": r.date,
                "user": {
                    "id": r.user.id,
                    "username": r.user.username
                },
                "items": fruits_data,
                "total": r.total
                })


        return jsonify(result)
    except Exception as ex:
        print(ex)
        return Response(status=500)





if __name__ == "__main__":
    app.run(host="localhost", debug=True)
