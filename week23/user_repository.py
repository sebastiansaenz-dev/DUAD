from sqlalchemy import select, func
from sqlalchemy.orm import Session, joinedload
from base_repository import BaseRepository
from models import Vehicles




class User_Repository(BaseRepository):

    def create(self, username, email, password):
        new_user = self.model(username=username, email=email, password=password)

        with session(self.engine) as session:
            session.add(new_user)
            session.commit()

    def get_users_with_multiple_vehicles(self):

        subq = (
            select(self.model.id)
            .join(self.model.vehicles)
            .group_by(self.model.id)
            .having(func.count(Vehicles.id) > 1)
            .scalar_subquery()
        )

        stmt = (
            select(self.model)
            .where(self.model.id.in_(subq))
            .order_by(self.model.username)
        )

        with Session(self.engine) as session:
            return session.execute(stmt).scalars().all()

    def get_all_addresses_and_vehicles(self, id):
        stmt = select(self.model).options(
            joinedload(self.model.vehicles),
            joinedload(self.model.address)
        ).where(self.model.id == id)

        with Session(self.engine) as session:
            return session.execute(stmt).unique().scalar_one_or_none()




