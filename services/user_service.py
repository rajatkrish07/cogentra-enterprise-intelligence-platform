import uuid
from models import UserORM
from logger import logger
from exceptions import NoEmailChangeError, DuplicateUsernameError
from repositories.user_repository import UserRepository

class UserService:

    def __init__(
            self,
            user_repository = UserRepository
    ):

        self.user_repository = user_repository

    # Creates user
    def create_user(self, user: UserORM) -> UserORM:

        if self.user_repository.get_by_email(user.email):
            raise DuplicateEmailError(user.email)

        if self.user_repository.get_by_username(user.username):
            raise DuplicateUsernameError(user.username)

        user.id = str(uuid.uuid4())
        created_user = self.user_repository.create_user(user)
        logger.info(f"User {user.username} created successfully!")
        return created_user

    # Updates user email
    def update_email(self, user: UserORM, new_email: str)->UserORM:
        if user.email == new_email:
            raise NoEmailChangeError()

        user.email = new_email
        updated_email = self.user_repository.update_email(user, new_email)
        logger.info(f"Email updated successfully to {user.email}.")
        return updated_email


