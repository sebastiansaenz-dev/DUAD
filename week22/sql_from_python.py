

from db import PgManager
from repositories import UserRepository, VehicleRepository, RentsRepository
from utils import export_csv, check_if_folder_exists
from datetime import datetime


#EXTRA EXERCISE 1
def export_db_to_csv():
    check_if_folder_exists('./db_backups')

    users_data = user_repo.get_all()
    vehicles_data = vehicle_repo.get_all()
    rents_data = rent_repo.get_all()

    time = datetime.now().strftime("%Y-%m-%d")

    export_csv(f'./db_backups/users_backup_{time}.csv', users_data, users_data[0].keys())
    export_csv(f'./db_backups/vehicles_backup_{time}.csv', vehicles_data, vehicles_data[0].keys())
    export_csv(f'./db_backups/rents_backup_{time}.csv', rents_data, rents_data[0].keys())

    print('data exported')


db_manager = PgManager(db_name="postgres", user="postgres", password="privado10", host="localhost")
user_repo = UserRepository(db_manager)
vehicle_repo = VehicleRepository(db_manager)
rent_repo = RentsRepository(db_manager)


export_db_to_csv()


db_manager.close_connection()

