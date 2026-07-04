from __future__ import annotations
import os
import json
from datetime import datetime
import logging
from pydantic import BaseModel, Field

logging.basicConfig(
    level = logging.INFO,
    format = "%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

# Custom Exception Classes
class ChatNotFoundError(Exception):
    pass

class MessageNotFoundError(Exception):
    pass

class DuplicateChatError(Exception):
    pass

class DuplicateEmailError(Exception):
    pass

class ChatRenameError(Exception):
    pass

# Manages all the operations like creating user and managing chats
class UserAccount(BaseModel):

  username: str
  email: str
  chats: list[Chat] = Field(default_factory=list)

  # Renaming or setting new email
  @property
  def email(self) -> str:
    return self.email

  @email.setter
  def email(self, new_email:str) -> None:
    if self.email != new_email:
      self.email = new_email
      logger.info(f"Email address changed successfully to {new_email}")

    else:
        raise DuplicateEmailError(f"Email '{new_email}' already exists.")

  # Display chats
  def display_chats(self) -> list:
    return self.chats.copy()

  # Creates new chat object
  def create_chat(self, title:str) -> None:
      if self.find_chat(title):
          raise DuplicateChatError(f"Chat '{title}' already exists.")

      chat_obj = Chat(title)
      self.chats.append(chat_obj)
      logger.info(f"Created new chat: {chat_obj.title}")

  # Find chats
  def find_chat(self, title:str) -> Chat | None:
      for my_chat in self.chats:
          if my_chat.title == title:
              return my_chat
      return None

  # Delete chats
  def delete_chat(self, title:str) -> None:
      chat = self.find_chat(title)
      if chat:
          self.chats.remove(chat)
          logger.info(f"Chat '{title}' deleted successfully.")
      else:
          raise ChatNotFoundError(f"Chat '{title}' not found.")

  # Displays user profile details (username and email)
  @property
  def profile(self) -> str:
    return f"Username: {self.username}\nEmail: {self.email}"

  def save(self, filename:str) -> None:
      with open(filename, "w") as my_file:
          json.dump(
              self.model_dump(),
              my_file,
              indent=4
          )
      logger.info(f"User data saved successfully to {filename}")

  @classmethod
  def load(cls, filename:str) -> UserAccount:
      with open(filename, "r") as my_file:
          my_dict = json.load(my_file)

      logger.info(f"User data loaded successfully from {filename}")
      return cls.model_validate(my_dict)

# Manages state of the chat like attributes and features
class Chat(BaseModel):
  
  title: str
  messages: list[Message] = Field(default_factory=list)

    # Display messages
  def display_messages(self) -> list:
      return self.messages.copy()

    # Adds new messages
  def add_message(self, text:str) -> None:
      timestamp = datetime.now()
      msg = Message(timestamp, text)
      self.messages.append(msg)
      logger.info(f"Message added to chat '{self.title}'.")

    # Edit existing messages
  def edit_message(self, text:str, new_text:str) -> None:
      for msg in self.messages:
          if msg.text == text:
              msg.text = new_text
              logger.info(f"Message edited successfully to '{self.title}'.")
              return

      raise MessageNotFoundError(f"Message '{text}' not found in chat '{self.title}'.")

    # Rename chats
  def rename_chat(self, new_title:str) -> None:
      if self.title != new_title:
          self.title = new_title
          logger.info(f"Chat renamed to '{self.title}'.")

      else:
          raise ChatRenameError(f"Chat '{new_title}' already exists.")

    # Deletes messages
  def delete_message(self, text:str) -> None:
      for msgs in self.messages:
          if msgs.text == text:
              self.messages.remove(msgs)
              logger.info(f"Message deleted successfully to {self.title}")
              return

      raise MessageNotFoundError(f"Message '{text}' not found in chat '{self.title}'.")

class Message(BaseModel):
  timestamp: datetime
  text: str



user = UserAccount("rajatkr_07", "rajatkrishnan2002@gmail.com")

# Creating Chats
user.create_chat("AI Masterclass")
user.create_chat("Master Python")
user.create_chat("JAVA Bootcamp")
print(user.display_chats())

#Deleting Chat with title "Master Python"

try:
    user.delete_chat("Python")
except ChatNotFoundError as e:
    print(e)

# Adding messages to the chats using title
chat = user.find_chat("JAVA Bootcamp")
chat.add_message("Welcome, Let's learn Java!")
chat.add_message("Crack Java SDE roles in 6 months")
chat.add_message("Are you excited??!!!")
print(type(chat.messages[0].timestamp))
print(type(chat.messages[0].model_dump()["timestamp"]))
print(chat.messages[0].model_dump())
print(chat.display_messages())

# Renaming Chats
user.find_chat("AI Masterclass").rename_chat("Advanced AI Masterclass")
print(user.display_chats())

# # Edit Message
user.find_chat("JAVA Bootcamp").edit_message("Crack Java SDE roles in 6 months", "Crack Java SDE roles in 8 months")
print(user.find_chat("JAVA Bootcamp").display_messages())

# Dumping python dictionary to json
user.save("user_data.json")

# Loading class back from json
user = UserAccount.load("user_data.json")

# Returns Class
print(user)

data = {
    "timestamp": "2026-07-05T10:30:00",
    "text": "Learning Pydantic"
}

msg = Message.model_validate(data)

print(msg)
print(type(msg.timestamp))
