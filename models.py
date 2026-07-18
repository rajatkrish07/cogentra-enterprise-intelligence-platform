from __future__ import annotations
import json
from datetime import datetime
from pydantic import BaseModel,Field,field_validator,EmailStr,ConfigDict,computed_field
from logger import logger
from exceptions import *


# Manages all the operations like creating user and managing chats
class UserAccount(BaseModel):
    username: str = Field(
        min_length=3,
        max_length=20,
    )
    email: EmailStr
    chats: list[Chat] = Field(
        default_factory=list
    )
    first_name: str = Field(
        min_length=1,
        max_length=50,
        alias="firstName"
    )

    last_name: str = Field(
        min_length=1,
        max_length=50,
        alias="lastName"
    )

    # Model Config: Raises ValidationError when an extra field is passed during object creation.
    model_config = ConfigDict(
        extra='forbid',
        validate_by_name=True
    )

    # Validates that username is not empty
    @field_validator("username")
    @classmethod
    def validate_username(cls, value) -> str:
        if value.strip() == "":
            raise ValueError("Username cannot be empty.")

        value = value.strip()
        return value

    # Validates that email is not empty
    @field_validator("email")
    @classmethod
    def validate_email(cls, value) -> EmailStr:
        if value.strip() == "":
            raise ValueError("Email cannot be empty.")

        return value

    # Validates that first name is not empty
    @field_validator("first_name")
    @classmethod
    def validate_first_name(cls, value) -> str:
        if value.strip() == "":
            raise ValueError("First name cannot be null.")

        return value

    # Validates that last name is not empty
    @field_validator("last_name")
    @classmethod
    def validate_last_name(cls, value) -> str:
        if value.strip() == "":
            raise ValueError("Last name cannot be null.")

        return value

    # Computing full name using first and last name
    @computed_field
    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    # Calculates number of chats
    @computed_field
    @property
    def chat_count(self) -> int:
        return len(self.chats)

    # Updates user email
    def update_email(self, new_email: EmailStr):
        if self.email != new_email:
            self.email = new_email
        else:
            raise DuplicateEmailError(f"Email '{new_email}' already exists.")
        logger.info(f"Email updated successfully to {new_email}.")

    # Display chats

    def display_chats(self) -> list:
        return self.chats.copy()

    # Creates new chat object
    def create_chat(self, title: str) -> None:
        if self.find_chat(title):
            raise DuplicateChatError(f"Chat '{title}' already exists.")

        chat_obj = Chat(title=title)
        self.chats.append(chat_obj)
        logger.info(f"Created new chat: {chat_obj.title}.")

    # Find chats
    def find_chat(self, title: str) -> Chat | None:
        for my_chat in self.chats:
            if my_chat.title == title:
                return my_chat
        return None

    # Delete chats
    def delete_chat(self, title: str) -> None:
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

    # Saving Pydantic model instance to python dictionary
    def save(self, filename: str) -> None:
        with open(filename, "w") as my_file:
            json.dump(
                self.model_dump(mode='json', round_trip=True),
                my_file,
                indent=4,
            )
        logger.info(f"User data saved successfully to {filename}.")

    # Loading back the dictionary to pydantic model instance
    @classmethod
    def load(cls, filename: str) -> UserAccount:
        with open(filename, "r") as my_file:
            my_dict = json.load(my_file)

        logger.info(f"User data loaded successfully from {filename}.")
        return cls.model_validate(my_dict)


# Manages state of the chat like attributes and features
class Chat(BaseModel):
    id: str = Field(min_length=1)
    title: str = Field(min_length=1, max_length=100)
    messages: list[Message] = Field(default_factory=list)

    # Model Config: Raises ValidationError when an extra field is passed during object creation.
    model_config = ConfigDict(
        extra='forbid',
        validate_by_alias=True
    )

    # Validates that username is not empty
    @field_validator("title")
    @classmethod
    def validate_title(cls, value) -> str:
        if value.strip() == "":
            raise ValueError("Chat title cannot be empty.")

        value = value.strip()
        return value

    # Computing message count
    @computed_field
    @property
    def message_count(self) -> int:
        return len(self.messages)

    # Display messages
    def display_messages(self) -> list:
        return self.messages.copy()

    # Adds new messages
    def add_message(self, text: str) -> None:
        timestamp = datetime.now()
        msg = Message(timestamp=timestamp, text=text)
        self.messages.append(msg)
        logger.info(f"Message added to chat '{self.title}'.")

    # Edit existing messages
    def edit_message(self, text: str, new_text: str) -> None:
        for msg in self.messages:
            if msg.text == text:
                msg.text = new_text
                logger.info(f"Message edited successfully to '{self.title}'.")
                return

        raise MessageNotFoundError(f"Message '{text}' not found in chat '{self.title}'.")

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


class Message(BaseModel):
    id: str = Field(min_length=1)
    timestamp: datetime
    text: str = Field(min_length=1, max_length=5000)

    # Model Config: Raises ValidationError when an extra field is passed during object creation.
    model_config = ConfigDict(
        extra='forbid'
    )

    @field_validator("text")
    @classmethod
    def validate_text(cls, value: str) -> str:
        if value.strip() == "":
            raise ValueError("Message text cannot be empty.")
        value = value.strip()
        return value

