from models import UserORM

class UserRepository:
    def __init__(self, db):
        self.db = db

    def create_user(self, user: UserORM) -> UserORM:
        self.db.add(user)
        self.db.commit()
        return user

    def update_email(self, user: UserORM, new_email: str)->UserORM:
        self.db.add(
            UserORM.id == user.id,
            UserORM.email == new_email
        )
        self.db.commit()
        return user