import uuid
from models import UserAccount, Chat
from logger import logger
from exceptions import DuplicateChatError, ChatNotFoundError, NoEmailChangeError
from pydantic import EmailStr

class UserService:

    # Find chats
    def find_chat(self, user: UserAccount, chat_id: str) -> Chat | None:
        for my_chat in user.chats:
            if my_chat.id == chat_id:
                return my_chat
        return None

    # Find chats by title
    def find_chat_by_title(self, user: UserAccount, title: str) -> Chat | None:
        for my_chat in user.chats:
            if my_chat.title == title:
                return my_chat
        return None

    # Creates new chat object
    def create_chat(self, user: UserAccount, title: str) -> Chat:
        if self.find_chat_by_title(user, title):
            raise DuplicateChatError(f"Chat '{title}' already exists.")

        chat = Chat(
            id = str(uuid.uuid4()),
            title=title
        )

        user.chats.append(chat)
        logger.info(f"Created new chat: {chat.title}.")
        return chat

    # Delete chats
    def delete_chat(self, user: UserAccount, chat_id: str) -> Chat:
        chat = self.find_chat(user, chat_id)
        if chat is None:
            raise ChatNotFoundError(f"Chat '{chat_id}' not found.")

        user.chats.remove(chat)
        logger.info(f"Chat '{chat_id}' deleted successfully.")
        return chat

    # Updates user email
    def update_email(self, user: UserAccount, new_email: EmailStr)->UserAccount:
        if user.email == new_email:
            raise NoEmailChangeError

        user.email = new_email
        logger.info(f"Email updated successfully to {user.email}.")
        return user


