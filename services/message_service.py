from datetime import datetime
import uuid
from exceptions import MessageNotFoundError
from logger import logger
from models import ChatORM, MessageORM
from repositories.message_repository import MessageRepository

class MessageService:
    def __init__(
            self,
            message_repository: MessageRepository
    ):
        self.message_repository = message_repository

#   Fetches message
    def get_message(
            self,
            message_id: str,
            ) -> MessageORM:

        message = self.message_repository.get(message_id)

        if message is None:
            raise MessageNotFoundError(message_id)

        return message

# Adds New Message
    def create_message(
            self,
            chat: ChatORM,
            text: str
    ) -> MessageORM:

        id = str(uuid.uuid4())
        timestamp = datetime.now()
        message = MessageORM(
            id=id,
            chat_id=chat.id,
            timestamp=timestamp,
            text=text
        )

        self.message_repository.create(message)
        logger.info(f"Message {id} added to chat {chat.id} successfully!")
        return message

# Edit existing messages
    def edit_message(self, message: MessageORM, new_text: str) -> MessageORM:
        message.text = new_text
        logger.info(f"Message {message.id} edited successfully!")
        self.message_repository.update(message)
        return message

# Deletes messages
    def delete_message(self, message: MessageORM) -> MessageORM:
            self.message_repository.delete(message)
            logger.info(f"Message {message.id} deleted successfully!")
            return message