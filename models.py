from __future__ import annotations
import json
from datetime import datetime
from pydantic import BaseModel, Field, field_validator, EmailStr, ConfigDict, computed_field
from logger import logger
from exceptions import (
    MessageNotFoundError,
    ChatRenameError
)

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


class Message(BaseModel):
    id: str = Field(min_length=1)
    chat_id: str = Field(min_length=1)
    timestamp: datetime
    text: str = Field(min_length=1, max_length=5000)
    responses: list[AIResponse] = Field(default_factory=list)

    # Model Config: Raises ValidationError when an extra field is passed during object creation.
    model_config = ConfigDict(
        extra='forbid'
    )

    @field_validator("text")
    @classmethod
    def validate_text(cls, value: str) -> str:
        value = value.strip()
        if value == "":
            raise ValueError("Message text cannot be empty.")
        return value

class AIResponse(BaseModel):
    id: str = Field(min_length=1)
    text: str = Field(min_length=1, max_length=5000)
    created_at: datetime

    @field_validator("text")
    @classmethod
    def validate_response_text(cls, value: str) -> str:
        value = value.strip()
        if value == "":
            raise ValueError("Response text cannot be empty.")
        return value

