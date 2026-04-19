
from sqlalchemy.orm import Session
from sqlalchemy import select
from extensions import db
from werkzeug.exceptions import NotFound



class BaseRepository:
    def __init__(self, model, schema):
        self.model = model
        self.schema = schema

    def to_dict(self, obj):

        if isinstance(obj, dict):
            data = obj
        else:
            data = obj.__dict__

        return {
            k: v for k, v in data.items() if not k.startswith('_') and v is not None
        }


    def get_all(self, filters):
        valid_filters = self.schema.load(filters, partial=True)

        valid_filters = self.to_dict(valid_filters)

        stmt = select(self.model).filter_by(**valid_filters)

        results = db.session.execute(stmt).scalars().unique().all()

        return self.schema.dump(results, many=True)

    def get_one(self, filters):

        stmt = select(self.model).filter_by(**filters)

        return db.session.execute(stmt).scalars().first()

    
    def get_by_id(self, id):
        result = db.session.get(self.model, id)

        return self.schema.dump(result)


    def create(self, data):
        new_item = self.schema.load(data)

        db.session.add(new_item)
        db.session.commit()
        db.session.refresh(new_item)
        return self.schema.dump(new_item)


    def update(self, id, data):
        stmt = select(self.model).where(self.model.id == id)

        item = db.session.execute(stmt).scalars().first()

        if not item:
            raise NotFound('item not found')

        updated_item = self.schema.load(data, instance=item, partial=True)
        db.session.commit()
        return self.schema.dump(updated_item)

    
    def delete(self, id):
        stmt = select(self.model).where(self.model.id == id)

        item = db.session.execute(stmt).scalars().first()

        if not item:
            raise NotFound('item not found')
        
        db.session.delete(item)
        db.session.commit()
        return True



##### CHANGE UPDATE FUNCTION TO FLUSH













