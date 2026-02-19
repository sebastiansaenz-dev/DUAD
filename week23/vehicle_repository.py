


from sqlalchemy import select
from sqlalchemy.orm import Session
from base_repository import BaseRepository
from models import Models, Users




class Vehicle_Repository(BaseRepository):

    def create(self, year, model_id):

        new_vehicle = self.model(year=year, model_id=model_id)

        with Session(self.engine) as session:
            session.add(new_vehicle)
            session.commit()

    def get_vehicles_without_user(self):
        stmt = select(
            self.model
        ).join(self.model.model).join(Models.make).outerjoin(self.model.user)

        stmt = stmt.where(Users.id.is_(None))

        with Session(self.engine) as session:
            return session.execute(stmt).scalars().all()







