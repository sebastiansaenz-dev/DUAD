



from sqlalchemy import create_engine, inspect
from user_repository import User_Repository
from vehicle_repository import Vehicle_Repository
from address_repository import Address_Repository
from vehicle_user_repository import Vehicle_User_Repository
from models import Base, Users, Addresses, Vehicles, Vehicles_Users


DB_URI = 'postgresql://postgres:privado10@localhost:5432/lyfter_cars'
engine = create_engine(DB_URI, echo=True)


def validate_tables():

    inspector = inspect(engine)

    tables_to_validate = ["Users", "Addresses", "Makes", "Models", "Vehicles", "Vehicles_users"]

    db_tables = inspector.get_table_names(schema="lyfter_cars")

    for table in tables_to_validate:
        if table not in db_tables:
            Base.metadata.create_all(engine)
    print('all tables are in the db')

try:
    validate_tables()
    user_repo = User_Repository(engine, Users)
    vehicle_repo = Vehicle_Repository(engine, Vehicles)
    address_repo = Address_Repository(engine, Addresses)
    vehicle_user_repo = Vehicle_User_Repository(engine, Vehicles_Users)

# EXERCISES

    # #Create/Modify/Delete user
    user_repo.create('Juan', 'juan@gmail.com', 'contra123')
    user_repo.update({"password": "new_password"}, {"username": "Juan"})
    user_repo.delete({"username": "Juan"})

    # #Create/Modify/Delete vehicle
    vehicle_repo.create(2025, 13)
    vehicle_repo.update({"year": 2026}, {"id": 2})
    vehicle_repo.delete({"id": 2})

    # #Create/Modify/Delete address
    address_repo.create('300 mts sur de ICE sabana', 1)
    address_repo.update({"address": "200 mts sur de ICE sabana"}, {"user_id": 1})
    address_repo.delete({"user_id": 1})

    # #Assign vehicle to user
    vehicle_user_repo.create(1, 3)

    # #Get all users
    user_repo.get_all()

    # #Get all vehicles
    vehicle_repo.get_all()

    # #Get all addresses
    address_repo.get_all()


    ######################################################

    # EXTRA EXERCISES

    # All vehicles with no user assigned
    vehicle_repo.get_vehicles_without_user()

    # All users with more than 1 vehicle
    user_repo.get_users_with_multiple_vehicles()

    #Get address with keyboard
    address_repo.get_address_by_keyword('300')

    #Get all directions and vehicles by user_id
    user_repo.get_all_addresses_and_vehicles(3)





except KeyError as ex:
    print(f'validation error: {ex}')

except Exception as ex:
    print(f'there was an error: {ex}')