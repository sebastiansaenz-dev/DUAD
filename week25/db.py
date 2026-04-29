from sqlalchemy import create_engine
from models import Users, Fruits, Receipts, Roles, ReceiptsFruits
from repos import FruitsRepository, UsersRepository, ReceiptsRepository, ReceiptsFruitsRepository, RolesRepository



class DB_Manager:
    def __init__(self, db_url):
        self.engine = create_engine(db_url)

        self.users = UsersRepository(self.engine, Users)
        self.fruits = FruitsRepository(self.engine, Fruits)
        self.receipts = ReceiptsRepository(self.engine, Receipts)
        self.receipts_fruits = ReceiptsFruitsRepository(self.engine, ReceiptsFruits)
        self.roles = RolesRepository(self.engine, Roles)
        