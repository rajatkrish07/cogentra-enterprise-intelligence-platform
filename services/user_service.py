import uuid
from models import UserORM
from logger import logger
from exceptions import NoEmailChangeError, DuplicateUsernameError, DuplicateEmailError
from repositories.user_repository import UserRepository
from sqlalchemy.exc import IntegrityError

class UserService:

    def __init__(
            self,
            user_repository = UserRepository
    ):

        self.user_repository = user_repository

    # Fetches user
    def search_user(
            self,
            user_id: str,
    )->UserORM:

        existing_user = self.user_repository.get_user(user_id)

        print("USERNAME:", user.username)
        print("EXISTING USER:", existing_username)

        if existing_user:
            return existing_user

        raise UserNotFoundError(user_id)

    # Creates user
    def create_user(self, user: UserORM) -> UserORM:

        if self.user_repository.get_by_email(user.email):
            raise DuplicateEmailError(user.email)

        if self.user_repository.get_by_username(user.username):
            raise DuplicateUsernameError(user.username)

        existing_username = self.user_repository.get_by_username(user.username)

        print("USERNAME CHECK:", user.username)
        print("FOUND:", existing_username)

        if existing_username:
            raise DuplicateUsernameError(user.username)

        user.id = str(uuid.uuid4())

        try:
            created_user = self.user_repository.create_user(user)

        except IntegrityError as exc:

            error_message = str(exc.orig)

            if "user_orm.email" in error_message:
                raise DuplicateEmailError(user.email)

            if "user_orm.username" in error_message:
                raise DuplicateUsernameError(user.username)

            raise

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


