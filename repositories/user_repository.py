from models import UserORM
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

class UserRepository:
    def __init__(self, db):
        self.db = db

    # Persists User
    def create_user(self, user: UserORM) -> UserORM:
        try:
            self.db.add(user)
            self.db.commit()

        except IntegrityError:
            self.db.rollback()
            raise

        return user

    # Fetches User
    def get_user(self, user_id: str) -> UserORM | None:
        stmt = select(UserORM).where(UserORM.id == user_id)
        execute = self.db.execute(stmt)
        result = execute.scalars().first()
        return result

    # Fetches user by email
    def get_by_email(self, email: str) -> UserORM | None:
        stmt = select(UserORM).where(UserORM.email == email)
        execute = self.db.execute(stmt)
        result = execute.scalars().first()
        return result

    # Fetches user by username
    def get_by_username(self, username: str) -> UserORM | None:
        stmt = select(UserORM).where(UserORM.username == username)
        execute = self.db.execute(stmt)
        result = execute.scalars().first()
        return result

    # Updates user email
    def update_email(self, user: UserORM, new_email: str)->UserORM:
        self.db.add(user)
        self.db.commit()
        return user