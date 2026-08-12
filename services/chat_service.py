import uuid
from datetime import datetime
from models import ChatORM, MessageORM
from logger import logger
from exceptions import ChatRenameError
from repositories.chat_repository import ChatRepository
from repositories.message_repository import MessageRepository

class ChatService:

    def __init__(
            self,
            chat_repo: ChatRepository,
            message_repo: MessageRepository
    ):

        self.chat_repo = chat_repo
        self.message_repo = message_repo

# Adds New Message
    def add_message(
            self,
            chat: ChatORM,
            text: str
    ) -> MessageORM:

        id = str(uuid.uuid4())
        timestamp = datetime.now()
        message = MessageORM(
            chat_id=chat.id,
            id=id,
            timestamp=timestamp,
            text=text
        )
        self.message_repo.create(message)
        logger.info(f"Message {id} added to chat .")
        return message

# Edit existing messages
    def edit_message(self, message: MessageORM, new_text: str) -> MessageORM:
        message.text = new_text
        logger.info(f"Message {message.id} edited successfully!")
        self.message_repo.update(message)
        return message

# Rename chats
    def rename_chat(self, chat: ChatORM, new_title: str) -> ChatORM:
        if chat.title == new_title:
            raise ChatRenameError("New title must be different from the current title.")
        chat.title = new_title
        self.chat_repo.update(chat)
        logger.info(f"Chat renamed to '{chat.title}'.")
        return chat

# Deletes messages
    def delete_message(self, message: MessageORM) -> MessageORM:
            self.message_repo.delete(message)
            logger.info(f"Message {message.id} deleted successfully!")
            return message
