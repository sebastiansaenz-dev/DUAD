

from .base_repo import BaseRepository
from models import UsersRoles, Users
from extensions import jwt_manager, bcrypt
from werkzeug.exceptions import Unauthorized, Conflict
from sqlalchemy import select


class UsersRepo(BaseRepository):
    def __init__(self, model, schema, session=None):
        super().__init__(model, schema, session)


    def register_user(self, data):
        try:

            validate_data = self.schema.load(data)

            username = validate_data.username
            email = validate_data.email
            password = validate_data.password

            username_stmt = select(Users).where(Users.username == username)
            username_exists = self.session.execute(username_stmt).scalars().first()

            email_stmt = select(Users).where(Users.email == email)
            email_exists = self.session.execute(email_stmt).scalars().first()


            if username_exists:
                raise Conflict('username already exists')

            if email_exists:
                raise Conflict('email already exists')
            
            
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

            new_user = self.model(
                username=username,
                email=email,
                password=hashed_password
            )

            self.session.add(new_user)
            self.session.flush()

            role_assignation = UsersRoles(user_id=new_user.id)
            self.session.add(role_assignation)

            self.session.refresh(new_user)

            self.session.commit()

            roles = [r.name for r in new_user.roles]

            payload = {
                'id': new_user.id,
                'roles': roles
            }

            token = jwt_manager.encode(payload)

            return {
                'user': self.schema.dump(new_user),
                'token': token
            }
        
        
        except Exception as ex:
            self.session.rollback()
            raise ex
        
    def login_user(self, data):
        try:
            email = data['email']
            password = data['password']

            user = self.get_one({'email': email})

            if not user or not bcrypt.check_password_hash(user.password, password):
                raise Unauthorized('invalid username or password')

            roles = [r.name for r in user.roles]

            payload = {
                'id': user.id,
                'roles': roles
            }

            token = jwt_manager.encode(payload)

            return {
                'user': self.schema.dump(user),
                'token': token
            }




        except Exception as ex:
            self.session.rollback()
            raise ex



























