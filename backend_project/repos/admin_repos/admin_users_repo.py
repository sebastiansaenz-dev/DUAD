



from repos.base_repo import BaseRepository
from models import UsersRoles, Roles, Users
from extensions import bcrypt, jwt_manager
from werkzeug.exceptions import NotFound, BadRequest, Conflict
from sqlalchemy import select, delete



class AdminUsersRepo(BaseRepository):
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

            if 'roles' in data:

                new_roles = data.pop('roles')

                roles_stmt = select(Roles)
                all_roles = self.session.execute(roles_stmt).scalars().all()

                roles_names = {role.name: role.id for role in all_roles}
                    

                for role in new_roles:
                    if role not in roles_names.keys():
                        raise BadRequest(f"role: {role} doesn't exists")
                    
                for role in new_roles:
                    role_id = roles_names[role]
                    new_role = UsersRoles(user_id=id, role_id=role_id)
                    self.session.add(new_role)

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


    def update_user(self, id, data):
        try:

            user_stmt = select(self.model).where(self.model.id == id)

            user = self.session.execute(user_stmt).scalars().unique().first()

            if not user:
                raise NotFound('user not found')

            if 'roles' in data:

                new_roles = data.pop('roles')

                roles_stmt = select(Roles)
                all_roles = self.session.execute(roles_stmt).scalars().all()

                roles_names = {role.name: role.id for role in all_roles}
                    

                for role in new_roles:
                    if role not in roles_names.keys():
                        raise BadRequest(f"role: {role} doesn't exists")

                delete_roles_stmt = delete(UsersRoles).where(UsersRoles.user_id == id)
                self.session.execute(delete_roles_stmt)
                    
                for role in new_roles:
                    role_id = roles_names[role]
                    new_role = UsersRoles(user_id=id, role_id=role_id)
                    self.session.add(new_role)

            self.schema.load(data, instance=user, partial=True)

            self.session.commit()
            self.session.refresh(user)

            return self.schema.dump(user)


        except Exception as ex:
            self.session.rollback()
            raise ex

    def delete_user(self, id):
        try:

            delete_roles_stmt = delete(UsersRoles).where(UsersRoles.user_id == id)
            self.session.execute(delete_roles_stmt)

            delete_user_stmt = delete(Users).where(Users.id == id)
            self.session.execute(delete_user_stmt)

            self.session.commit()

            return True


        except Exception as ex:
            self.session.rollback()
            print(ex)
            raise ex

















