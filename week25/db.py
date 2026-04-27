from sqlalchemy import create_engine
from sqlalchemy import select, update, delete
from sqlalchemy.orm import Session
from models import Users, Fruits, Receipts, Roles, ReceiptsFruits
from repos import FruitsRepository, UsersRepository, ReceiptsRepository, ReceiptsFruitsRepository, RolesRepository



class DB_Manager:
    def __init__(self):
        self.engine = create_engine('postgresql+psycopg2://postgres:privado10@localhost:5432/jwt_exercises')

        self.users = UsersRepository(self.engine, Users)
        self.fruits = FruitsRepository(self.engine, Fruits)
        self.receipts = ReceiptsRepository(self.engine, Receipts)
        self.receipts_fruits = ReceiptsFruitsRepository(self.engine, ReceiptsFruits)
        self.roles = RolesRepository(self.engine, Roles)
        