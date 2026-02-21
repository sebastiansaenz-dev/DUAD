
from sqlalchemy import select, update, delete
from sqlalchemy.orm import Session

class BaseRepository():
    def __init__(self, engine, model):
        self.engine = engine
        self.model = model

    def _apply_filters(self, stmt, filters):
        for key, value in filters.items():
            if hasattr(self.model, key):
                column = getattr(self.model, key)
                stmt = stmt.where(column == value)
            else:
                raise KeyError(f'column does not exists: {key}')
        return stmt
    
    def get_all(self, filters=None):
        stmt = select(self.model)

        if filters:
            stmt = self._apply_filters(stmt, filters)

        with self.engine.connect() as conn:
            result = conn.execute(stmt)
            return result.mappings().all()
        
    def update(self, values, filters):

        valid_data = {
            key: value for key, value in values.items()
            if hasattr(self.model, key)
        }

        if not valid_data:
            return
        
        stmt = update(self.model).values(**valid_data)

        stmt = self._apply_filters(stmt, filters)

        with Session(self.engine) as session:
            session.execute(stmt)
            session.commit()


    def delete(self, filters):

        stmt = delete(self.model)

        stmt = self._apply_filters(stmt, filters)

        with Session(self.engine) as session:
            session.execute(stmt)
            session.commit()



