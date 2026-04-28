
from sqlalchemy import MetaData, Column, Integer, String, DateTime, func, ForeignKey
from sqlalchemy.orm import DeclarativeBase, relationship




class Base(DeclarativeBase):
    metadata = MetaData(schema='jwt_exercises')


class ReceiptsFruits(Base):
    __tablename__ = "Receipts_fruits"
    id = Column(Integer, primary_key=True)
    fruit_id = Column(Integer, ForeignKey("Fruits.id"), nullable=False)
    receipt_id = Column(Integer, ForeignKey("Receipts.id"), nullable=False)
    quantity = Column(Integer, nullable=False)

    receipt = relationship("Receipts", back_populates='receipts_fruits')
    fruits = relationship("Fruits", back_populates='receipts', lazy='joined')


class Users(Base):
    __tablename__ = "Users"
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    role_id = Column(Integer, ForeignKey("Roles.id"), nullable=False, default=1, server_default="1")

    receipts = relationship("Receipts", back_populates="user")
    roles = relationship("Roles", back_populates="user", lazy="joined")

    __hidden__ = ['password']


class Fruits(Base):
    __tablename__ = "Fruits"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    entry_date = Column(DateTime, server_default=func.now())
    quantity = Column(Integer, nullable=False)

    receipts = relationship("ReceiptsFruits", back_populates="fruits")

    __hidden__ = ['entry_date']


class Receipts(Base):
    __tablename__ = "Receipts"
    id = Column(Integer, primary_key=True)
    date = Column(DateTime, server_default=func.now())
    user_id = Column(Integer, ForeignKey("Users.id"))
    total = Column(Integer, nullable=False)

    user = relationship("Users", back_populates="receipts")
    receipts_fruits = relationship("ReceiptsFruits", back_populates='receipt', lazy='joined')


class Roles(Base):
    __tablename__ = "Roles"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    user = relationship("Users", back_populates="roles")