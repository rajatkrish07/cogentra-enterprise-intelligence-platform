from models import UserAccount, Chat
from logger import logger
from exceptions import DuplicateChatError


class UserService:

    def find_chat(self, user: UserAccount, chat_id: str) -> Chat | None:
        for my_chat in user.chats:
            if my_chat.id == chat_id:
                return my_chat
        return None

    def find_chat_by_title(self, user: UserAccount, title: str) -> Chat | None:
        for my_chat in user.chats:
            if my_chat.title == title:
                return my_chat
        return None

    def create_chat(self, user: UserAccount, title: str) -> Chat:
        if self.find_chat_by_title(user, title):
            raise DuplicateChatError(f"Chat '{title}' already exists.")

        chat = Chat(title=title)
        user.chats.append(chat)
        logger.info(f"Created new chat: {chat.title}.")
        return chat


