


from sqlalchemy.orm import Session
from base_repository import BaseRepository




class Vehicle_User_Repository(BaseRepository):
    def create(self, vehicle_id, user_id):
        new_vehicle_user = self.model(vehicle_id=vehicle_id, user_id=user_id)

        try:
            with Session(self.engine) as session:
                session.add(new_vehicle_user)
                session.commit()
        except Exception as ex:
            print(f'error assigning vehicle: {ex}')




