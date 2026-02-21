

from sqlalchemy.orm import Session
from base_repository import BaseRepository




class Make_Repository(BaseRepository):
    def create(self, name):
        new_make = self.model(name=name)

        with Session(self.engine) as session:
            session.add(new_make)
            session.commit()






