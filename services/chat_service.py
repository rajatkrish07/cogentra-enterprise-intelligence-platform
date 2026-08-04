from datetime import datetime
from models import Chat, Message
from logger import logger
from exceptions import MessageNotFoundError, ChatRenameError

# Adds new messages

class ChatService:

    def add_message(self, chat: Chat, text: str) -> Message:
        timestamp = datetime.now()
        msg = Message(timestamp=timestamp, text=text)
        chat.messages.append(msg)
        logger.info(f"Message added to chat '{chat.title}'.")
        return msg

    # Edit existing messages
    def edit_message(self, message: Message, new_text: str) -> Message:
        message.text = new_text
        logger.info(f"Message {message.id} edited successfully!")
        return message

    # Rename chats
    def rename_chat(self, new_title: str) -> None:
        if self.title != new_title:
            self.title = new_title
            logger.info(f"Chat renamed to '{self.title}'.")

        else:
            raise ChatRenameError(f"Chat '{new_title}' already exists.")

    # Deletes messages
    def delete_message(self, text: str) -> None:
        for msgs in self.messages:
            if msgs.text == text:
                self.messages.remove(msgs)
                logger.info(f"Message deleted successfully to {self.title}")
                return

        raise MessageNotFoundError(f"Message '{text}' not found in chat '{self.title}'.")