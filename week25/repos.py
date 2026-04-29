

from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select, update, delete




class BaseRepository():
    def __init__(self, engine, model):
        self.engine = engine
        self.model = model

    def _apply_filters(self, stmt, filters):
        try:
            if not filters:
                return None
            
            if not any(hasattr(self.model, k) for k in filters):
                return None
            for key, value in filters.items():
                if hasattr(self.model, key):
                    column = getattr(self.model, key)
                    stmt = stmt.where(column == value)
            return stmt
        except Exception as ex:
            print(f'Error: {ex}')


    def get_all(self, filters=None):
        stmt = select(self.model)

        if filters:
            stmt = self._apply_filters(stmt, filters)

        if stmt is None:
            return []

        with Session(self.engine) as session:
            return session.execute(stmt).scalars().all()
        
    
    def get_by_id(self, id):

        stmt = (
            select(self.model)
            .where(self.model.id == id)
        )

        with Session(self.engine) as session:
            item = session.execute(stmt).scalars().unique().first()
            if item:
                session.expunge(item)
                return item
        return None

    def create(self, data):
        valid_data = {
            key: value for key, value in data.items()
            if hasattr(self.model, key)
        }

        new_item = self.model(**valid_data)

        with Session(self.engine) as session:
            session.add(new_item)
            session.commit()
            session.refresh(new_item)
            session.expunge(new_item)
        return new_item

    def update(self, values, filters):

        valid_data = {
            key: value for key, value in values.items()
            if hasattr(self.model, key)
        }

        if not valid_data:
            return

        stmt_update = update(self.model).values(**valid_data)
        stmt_update = self._apply_filters(stmt_update, filters)

        stmt_select = select(self.model)
        stmt_select = self._apply_filters(stmt_select, filters)

        if stmt_update is None:
            return False

        with Session(self.engine) as session:
            session.execute(stmt_update)

            updated_items = session.execute(stmt_select).scalars().all()

            if updated_items:
                session.commit()
                for item in updated_items:
                    session.refresh(item)
                    session.expunge(item)
                return updated_items
            
            session.commit()


    def delete(self, filters):
        stmt = delete(self.model)

        stmt = self._apply_filters(stmt, filters)

        if stmt is None:
            return False

        with Session(self.engine) as session:
            results = session.execute(stmt)
            session.commit()
            if results.rowcount == 0:
                raise LookupError('item not found')
            return True


    def to_dict(self, obj, ignore_hidden=False):

        hidden = [] if ignore_hidden else getattr(obj, '__hidden__', [])

        converted_obj = {c.name: getattr(obj, c.name) for c in obj.__table__.columns if c.name not in hidden}

        return converted_obj


class FruitsRepository(BaseRepository):
    def get_all(self, filters=None):
        stmt = select(self.model).where(self.model.is_active == True)

        if filters:
            stmt = self._apply_filters(stmt, filters)

        if stmt is None:
            return []

        with Session(self.engine) as session:
            return session.execute(stmt).scalars().all()
        
    def delete(self, id):
        stmt = select(self.model).where(self.model.id == id)

        with Session(self.engine) as session:
            fruit = session.execute(stmt).scalars().first()
            if fruit is None:
                return False
            fruit.is_active = False
            session.commit()
            return True


class UsersRepository(BaseRepository):
    def get_all(self, filters, load_role=False):
        stmt = select(self.model)

        if filters:
            stmt = self._apply_filters(stmt, filters)

        if load_role:
            stmt = stmt.options(joinedload(self.model.roles))

        if stmt is None:
            return []

        with Session(self.engine) as session:
            return session.execute(stmt).scalars().all()


    def get_by_id(self, id, load_role=False):
        stmt = select(self.model).where(self.model.id == id)

        if load_role:
            stmt = stmt.options(joinedload(self.model.roles))

        with Session(self.engine) as session:
            return session.execute(stmt).scalars().first()

class ReceiptsRepository(BaseRepository):
    def get_all(self, filters, load_user=False, load_fruits=False):
        stmt = select(self.model)

        if filters:
            stmt = self._apply_filters(stmt, filters)

        if load_user:
            stmt = stmt.options(joinedload(self.model.user))
        
        if load_fruits:
            stmt = stmt.options(joinedload(self.model.receipts_fruits))

        with Session(self.engine) as session:
            return session.execute(stmt).scalars().unique().all()
        
    def get_by_id(self, id, load_user=False, load_fruits=False):
        stmt = select(self.model).where(self.model.id == id)

        if load_user:
            stmt = stmt.options(joinedload(self.model.user))

        if load_fruits:
            stmt = stmt.options(joinedload(self.model.fruits))

        with Session(self.engine) as session:
            return session.execute(stmt).scalars().first()

class ReceiptsFruitsRepository(BaseRepository):
    pass

class RolesRepository(BaseRepository):
    pass



