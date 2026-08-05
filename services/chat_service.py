import uuid
from datetime import datetime
from models import Chat, Message
from logger import logger
from exceptions import MessageNotFoundError, ChatRenameError

# Adds new messages

class ChatService:

# Adds New Message
    def add_message(
            self,
            chat: Chat,
            text: str
    ) -> Message:

        id = str(uuid.uuid4())
        timestamp = datetime.now()
        msg = Message(
            chat_id=chat.id,
            id=id,
            timestamp=timestamp,
            text=text
        )
        chat.messages.append(msg)
        logger.info(f"Message {id} added to chat .")
        return msg

# Edit existing messages
    def edit_message(self, message: Message, new_text: str) -> Message:
        message.text = new_text
        logger.info(f"Message {message.id} edited successfully!")
        return message

# Rename chats
    def rename_chat(self, chat: Chat, new_title: str) -> Chat:
        if chat.title == new_title:
            raise ChatRenameError("New title must be different from the current title.")
        chat.title = new_title
        logger.info(f"Chat renamed to '{chat.title}'.")
        return chat

# Deletes messages
    def delete_message(self, chat: Chat, message: Message) -> Message:
            chat.messages.remove(message)
            logger.info(f"Message {message.id} deleted successfully!")
            return message
