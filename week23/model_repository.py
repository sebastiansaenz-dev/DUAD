


from sqlalchemy.orm import Session
from base_repository import BaseRepository



class Model_Repository(BaseRepository):
    def create(self, name, make_id):

        new_model = self.model(name=name, make_id=make_id)

        with Session(self.engine) as session:
            session.add(new_model)
            session.commit()








