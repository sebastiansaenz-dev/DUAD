

from sqlalchemy import Column, Integer, String, ForeignKey, MetaData
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    metadata = MetaData(schema="lyfter_cars")


class Vehicles_Users(Base):
    __tablename__ = "Vehicles_users"
    id = Column(Integer, primary_key=True)
    vehicle_id = Column(Integer, ForeignKey("Vehicles.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("Users.id"), nullable=False)


class Users(Base):
    __tablename__ = "Users"
    id = Column(Integer, primary_key=True)
    username = Column("username", String(50), nullable=False)
    email = Column("email", String(255), nullable=False)
    password = Column("password", String, nullable=False)

    address = relationship("Addresses", back_populates="user")
    vehicles = relationship("Vehicles", secondary=Vehicles_Users.__table__, back_populates="user")


class Addresses(Base):
    __tablename__ = "Addresses"
    id = Column(Integer, primary_key=True)
    address = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("Users.id"), nullable=False)

    user = relationship("Users", back_populates="address")


class Makes(Base):
    __tablename__ = "Makes"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)

    model = relationship("Models", back_populates="make")


class Models(Base):
    __tablename__ = "Models"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    make_id = Column(Integer, ForeignKey("Makes.id"), nullable=False)

    vehicles = relationship("Vehicles", back_populates="model")
    make = relationship("Makes", back_populates="model")


class Vehicles(Base):
    __tablename__ = "Vehicles"
    id = Column(Integer, primary_key=True)
    year = Column(Integer, nullable=False)
    model_id = Column(Integer, ForeignKey("Models.id"), nullable=False)

    user = relationship("Users", secondary=Vehicles_Users.__table__, back_populates="vehicles")
    model = relationship("Models", back_populates="vehicles")











