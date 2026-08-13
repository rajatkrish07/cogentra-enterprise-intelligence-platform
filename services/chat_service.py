import uuid
from exceptions import DuplicateChatError, ChatRenameError
from models import ChatORM
from logger import logger
from exceptions import ChatRenameError
from repositories.chat_repository import ChatRepository

class ChatService:

    def __init__(
            self,
            chat_repository: ChatRepository
    ):

        self.chat_repository = chat_repository

    # Finds Chat by ID
    def find_chat(self, chat_id: str) -> ChatORM | None:
        chat = self.chat_repository.get_chat(chat_id)
        return chat

    # Find chats by Title
    def find_chat_by_title(self, title: str) -> ChatORM | None:
        chat = self.chat_repository.get_chat_by_title(title)
        return chat

    # Creates new chat object
    def create_chat(self, user_id: str, title: str) -> ChatORM:
        # if self.find_chat_by_title(user, title):
        existing_chat = self.chat_repository.get_chat_by_title(
            user_id = user_id,
            title = title
        )

        if existing_chat:
            raise DuplicateChatError("Chat title already exists.")

        chat = ChatORM(
            id = str(uuid.uuid4()),
            user_id = user_id,
            title=title
        )

        created_chat = self.chat_repository.create(chat)
        logger.info(f"Created new chat: {chat.title}.")
        return created_chat

    # Delete chats
    def delete_chat(self, chat: ChatORM) -> ChatORM:
        deleted_chat = self.chat_repository.delete(chat)
        logger.info(f"Chat '{chat.id}' deleted successfully.")
        return deleted_chat

    # Rename chats
    def rename_chat(self, chat: ChatORM, new_title: str) -> ChatORM:
        if chat.title == new_title:
            raise ChatRenameError("New title must be different from the current title.")

        chat.title = new_title
        self.chat_repository.update(chat)
        logger.info(f"Chat renamed to '{chat.title}'.")
        return chat