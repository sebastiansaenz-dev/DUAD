


class UserRepository:
    def __init__(self, db_manager):
        self.db_manager = db_manager


    def _format_user(self, user_record):
        return {
            "id": user_record[0],
            "name": user_record[1],
            "email": user_record[2],
            "username": user_record[3],
            "password": user_record[4],
            "birthday": user_record[5],
            "status": user_record[6]
        }

    def get_all(self, filters=None):

        query = 'SELECT users.id, users.name, users.email, users.username, users.password, users.birthday, status.name FROM lyfter_car_rental."Users" AS users JOIN lyfter_car_rental."User_status" AS status ON users.status_id = status.id'

        params = []
        where_clauses = []

        allowed_filters = {
            "id": "users.id",
            "name": "users.name",
            "email": "users.email",
            "username": "users.username",
            "birthday": "users.birthday",
            "status": "status.name"
        }

        if filters:
            for key, value in filters.items():
                if key in allowed_filters and value is not None:
                    where_clauses.append(f'{allowed_filters[key]} = %s')
                    params.append(value)

        if where_clauses:
            query += " WHERE " + " AND ".join(where_clauses)



        try:
            results = self.db_manager.execute_query(query, tuple(params))
            return [self._format_user(u) for u in results]
        except Exception as ex:
            print(f'Error getting users: {ex}')
            return False
    
    def create(self, name, email, username, password, birthday):
        try:
            self.db_manager.execute_query(
                'INSERT INTO lyfter_car_rental."Users" (name, email, username, password, birthday) VALUES (%s, %s, %s, %s, %s)', (name, email, username, password, birthday)
            )
            print('user inserted')
            return True
        except Exception as ex:
            print(f'Error creating user: {ex}')
            return False
        
    def update_status(self, _id, status_id):
        try:
            self.db_manager.execute_query(
                'UPDATE lyfter_car_rental."Users" SET status_id = %s WHERE id = %s', (status_id, _id)
            )
            print('User updated')
            return True
        except Exception as ex:
            print(f'Error updating user: {ex}')
            return False
        
    def flag_delinquet_user(self, _id):
        try:
            self.db_manager.execute_query(
                'UPDATE lyfter_car_rental."Users" SET status_id = %s WHERE id = %s', (3, _id)
            )
            print('User updated')
            return True
        except Exception as ex:
            print(f'Error updating user: {ex}')
            return False
    
        

class VehicleRepository:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def _format_vehicle(self, vehicle_record):
        return {
            "id": vehicle_record[0],
            "model": {
                "status_id": vehicle_record[1],
                "name": vehicle_record[2]
            },
            "year": vehicle_record[3],
            "status": {
                "id": vehicle_record[4],
                "name": vehicle_record[5]
            }
        }
    
    def get_all(self, filters=None):

        query = 'SELECT vehicle.id, vehicle.model_id, models.name AS model_name, vehicle.year, vehicle.status_id, status.name AS status_name FROM lyfter_car_rental."Vehicles" AS vehicle JOIN lyfter_car_rental."Models" AS models ON vehicle.model_id = models.id JOIN lyfter_car_rental."Vehicle_status" AS status ON vehicle.status_id = status.id'

        params = []
        where_clauses = []

        allowed_filters = {
            "id": "vehicle.id",
            "model_id": "vehicle.model_id",
            "model_name": "models.name",
            "year": "vehicle.year",
            "status": "status.name"
        }


        if filters:
            for key, value in filters.items():
                if key in allowed_filters and value is not None:
                    where_clauses.append(f'{allowed_filters[key]} = %s')
                    params.append(value)

        if where_clauses:
            query += " WHERE " + " AND ".join(where_clauses)



        try:
            results = self.db_manager.execute_query(query, tuple(params))
            return [self._format_vehicle(v) for v in results]
        except Exception as ex:
            print(f'Error getting all vehicles: {ex}')
            return False

    def create(self, model_id, year, status_id):
        try:
            self.db_manager.execute_query(
                'INSERT INTO lyfter_car_rental."Vehicles" (model_id, year, status_id) VALUES (%s, %s, %s)', (model_id, year, status_id)
            )
            print('Vehicle inserted')
            return True
        except Exception as ex:
            print(f'Error creating vehicle: {ex}')
            return False

    def update_status(self, _id, status_id):
        try:
            self.db_manager.execute_query(
                'UPDATE lyfter_car_rental."Vehicles" SET status_id = %s WHERE id = %s', (status_id, _id)
            )
            print('Vehicle updated')
            return True
        except Exception as ex:
            print(f'Error updating vehicle: {ex}')
            return False 
        

class RentsRepository:
    def __init__(self, db_manager):
        self.db_manager = db_manager


    def create(self,  vehicle_id, user_id):
        try:
            self.db_manager.execute_query(
                'INSERT INTO lyfter_car_rental."Rents" (vehicle_id, user_id) VALUES (%s, %s)', (vehicle_id, user_id)
            )
            print('rent inserted')
            return True
        except Exception as ex:
            print(f'Error creating rent: {ex}')
            return False
        
    def complete_rent(self, _id):
        try:
            self.db_manager.execute_query(
                'UPDATE lyfter_car_rental."Rents" SET status_id = %s WHERE id = %s', (5, _id)
            )
            print('Rent completed')
            return True
        
        except Exception as ex:
            print(f'Error completing rent: {ex}')
            return False

    def update_status(self, _id, status_id):
        try:
            self.db_manager.execute_query(
                'UPDATE lyfter_car_rental."Rents" SET status_id = %s WHERE id = %s', (status_id, _id)
            )
            print('Rent updated')
            return True
        except Exception as ex:
            print(f'Error updating rent: {ex}')
            return False
        
    def _format_rent(self, rent_record):
        return {
            "id": rent_record[0],
            "vehicle_id": rent_record[1],
            "model": {
                "name": rent_record[2]
            },
            "user": {
                "id": rent_record[3],
                "name": rent_record[4]
            },
            "date": rent_record[5],
            "status": rent_record[6]
        }

    def get_all(self, filters=None):
        query = 'SELECT rent.id, vehicle.id, model.name AS model, users.id AS user_id, users.name AS user_name, rent.date, status.name AS status FROM lyfter_car_rental."Rents" AS rent JOIN lyfter_car_rental."Vehicles" AS vehicle ON vehicle.id = rent.vehicle_id JOIN lyfter_car_rental."Models" AS model ON vehicle.model_id = model.id JOIN lyfter_car_rental."Users" AS users ON users.id = rent.user_id JOIN lyfter_car_rental."Rent_status" AS status ON rent.status_id = status.id'

        params = []
        where_clauses = []

        allowed_filters = {
            "id": 'rent.id',
            "vehicle_id": 'rent.vehicle_id',
            "model": 'model.name',
            "user_id": 'rent.user_id',
            "user_name": 'users.name',
            "rent_date": 'rent.date',
            "status": 'status.name'
        }

        if filters:
            for key, value in filters.items():
                if key in allowed_filters and value is not None:
                    where_clauses.append(f"{allowed_filters[key]} = %s")
                    params.append(value)

        if where_clauses:
            query += " WHERE " + " AND ".join(where_clauses)


        try:
            results = self.db_manager.execute_query(query, tuple(params))
            return [self._format_rent(r) for r in results]
        except Exception as ex:
            print(f'Error getting rents: {ex}')
            return False
        


