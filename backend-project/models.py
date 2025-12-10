

from datetime import date as SystemDate

date = 0

class Model():

    _id_counter = 0


    @classmethod
    def next_id(cls, existing_objects=None):
        if existing_objects:
            cls._id_counter = max(obj.id for obj in existing_objects)
        cls._id_counter += 1
        return cls._id_counter
    
    
    @classmethod
    def exists_in_list(cls, object_to_check, existing_objects, key):
        return any(getattr(obj, key) == getattr(object_to_check, key) for obj in existing_objects)


    def to_json(self):
        result = {}
        for key, value in self.__dict__.items():
            if isinstance(value, list):
                result[key] = [
                    item.to_json() if isinstance(item, Model) else item for item in value
                ]
            elif isinstance(value, Model):
                result[key] = value.to_json()
            else:
                result[key] = value
        return result
    

    @classmethod
    def from_json(cls, data, types_map=None):
        
        types_map = types_map or {}
        obj_data = {}
        for key, value in data.items():
            if key in types_map:
                if isinstance(value, list):
                    obj_data[key] = [types_map[key].from_json(v) for v in value]
                else:
                    obj_data[key] = types_map[key].from_json(value)
            else:
                obj_data[key] = value
        return cls(**obj_data)


class User(Model):
    def __init__(self, id, username, password, role='user', created_at=None):
        self.id = id
        self.username = username
        self.password = password
        self.role = role
        self.created_at = created_at or str(SystemDate.today())


class Receipt(Model):
    def __init__(self, id, code, sale_id, products, total, payment_method, date=None):
        self.id = id
        self.code = code
        self.sale_id = sale_id
        self.products = products
        self.total = total
        self.payment_method = payment_method
        self.date = date or str(SystemDate.today())

    def to_public_json(self, products_list):
        return {
            'code': self.code,
            'date': self.date,
            'items': [
                {
                    'product_id': item.product_id,
                    'name': next(p.name for p in products_list if p.id == item.product_id),
                    'price': next(p.price for p in products_list if p.id == item.product_id),
                    'quantity': item.quantity
                }
                for item in self.products
            ],
            'total': self.total
        }


class Product(Model):
    def __init__(self, id, code, name, price, brand, stock, entry_date=None):
        self.id = id
        self.code = code
        self.name = name
        self.price = float(price)
        self.brand = brand
        self.stock = int(stock)
        self.entry_date = entry_date or str(SystemDate.today())


    def restock(self, amount):
        self.stock += int(amount)

    
    def reduce_stock(self, amount):
        if self.stock < amount:
            raise ValueError('not enough stock available')
        self.stock -= int(amount)


class Sale(Model):
    def __init__(self, id , user_id, products, total, date, payment_method, refund_status=False):
        self.id = id
        self.user_id = user_id
        self.products = products
        self.total = total
        self.date = date or str(SystemDate.today())
        self.payment_method = payment_method
        self.refund_status = refund_status

    @staticmethod
    def calculate_total(cart_items, products_list):
        product_map = {p.id: p for p in products_list}

        total = 0

        for ci in cart_items:
            product = product_map.get(ci.product_id)
            if not product:
                raise ValueError(f'product_id {product.id} not found')
            total += product.price * ci.quantity
        return total


class Cart(Model):
    def __init__(self, id, user_id, products=None):
        self.id = id
        self.user_id = user_id
        self.products = products or []

    def get_total(self, products_list):
        total = 0

        product_map = {p.id: p for p in products_list}

        for item in self.products:
            product = product_map.get(item.product_id)
            if product:
                total += product.price * item.quantity
        
        return total
    
    def empty_cart(self):
        self.products = []


class CartItem(Model):
    def __init__(self, id, product_id, quantity):
        self.id = id
        self.product_id = product_id
        self.quantity = quantity


class Refund(Model):
    def __init__(self, id, sale_id, products, total=0, date=None):
        self.id = id
        self.sale_id = sale_id
        self.products = products
        self.date = date or str(SystemDate.today())
        self.total = total

    @staticmethod
    def total_refund(refund_items, products_list):
        product_map = {p.id: p for p in products_list}

        total = 0

        for ri in refund_items:
            product = product_map.get(ri.product_id)

            if not product:
                raise ValueError(f'product_id {product.id} not found')
            total -= product.price * ri.quantity

        return total
