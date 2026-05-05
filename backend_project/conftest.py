
import pytest
from sqlalchemy import create_mock_engine
from extensions import db as _db
from app import create_app
from sqlalchemy.orm import sessionmaker

@pytest.fixture(scope='session')
def app():
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'REDIS_HOST': None
    })

    return app


@pytest.fixture(scope='session')
def db(app):
    with app.app_context():

        if _db.engine.url.drivername == 'sqlite':
            for table in _db.metadata.tables.values():
                table.schema = None

        _db.create_all()
        yield _db
        _db.drop_all()


@pytest.fixture()
def session(db, app):
    with app.app_context():
        connection = db.engine.connect()
        transaction = connection.begin()

        Session = sessionmaker(bind=connection)
        session = Session()


        yield session

        session.close()
        transaction.rollback()
        connection.close()













