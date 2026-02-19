


from sqlalchemy import select
from sqlalchemy.orm import Session
from base_repository import BaseRepository



class Address_Repository(BaseRepository):

    def create(self, address, user_id):
        new_user = self.model(address=address, user_id=user_id)

        with Session(self.engine) as session:
            session.add(new_user)
            session.commit()


    def get_address_by_keyword(self, keyword):

        stmt = select(
            self.model
        ).where(
            self.model.address.ilike(f"%{keyword}%")
        )

        with Session(self.engine) as session:
            return session.execute(stmt).scalars().all()
