from models import ChatORM, MessageORM, UserORM
from exceptions import ChatNotFoundError, MessageNotFoundError, UserNotFoundError
from fastapi import Depends, Path
from database.database import SessionLocal
from repositories.user_repository import UserRepository
from services.ai_response_service import AIService
from services.chat_service import ChatService
from repositories.ai_response_repository import AIResponseRepository
from repositories.chat_repository import ChatRepository
from repositories.message_repository import MessageRepository
from services.message_service import MessageService
from services.user_service import UserService

# Repository dependency

# Creating session instance
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

# Assigning/Allocating session to UserRepository
def get_user_repository(
        db = Depends(get_db)
):
    return UserRepository(db)

# Assigning/Allocating session to UserService
def get_user_service(
        user_repository: UserRepository = Depends(get_user_repository)
):
    return UserService(user_repository)

# Assigning/Allocating session to ChatRepository
def get_chat_repository(
        db = Depends(get_db)
):
    return ChatRepository(db)

# Assigning/Allocating session to ChatService
def get_chat_service(
        chat_repository: ChatRepository = Depends(get_chat_repository),
) -> ChatService:
    return ChatService(chat_repository)

# Assigning/Allocating session to MessageRepository
def get_message_repository(
        db = Depends(get_db)
):
    return MessageRepository(db)

# Assigning/Allocating session to MessageService
def get_message_service(
        message_repository: MessageRepository = Depends(get_message_repository),
) -> MessageService:
    return MessageService(message_repository)

# Assigning/Allocating session to AIResponseRepository
def get_ai_response_repository(
        db = Depends(get_db)
):
    return AIResponseRepository(db)

# Assigning/Allocating session to AIService
def get_ai_service(
        repository: AIResponseRepository = Depends(get_ai_response_repository)
)-> AIService:
    return AIService(repository)

# Returns API Version
def get_api_version() -> str:
    return "v1"

# Gets user by id
def get_user(
        user_id: str = Path(
            ...,
            min_length=1,
            title="User ID",
            description="Unique identifier of the user",
        ),
        user_repository: UserRepository = Depends(get_user_repository)
)-> UserORM:

    # Asks User Repository to fetch result from DB
    user = user_repository.get_user(user_id)

    # Validation: If found then chat is returned, otherwise UserNotFound exception
    if user is None:
        raise UserNotFoundError()

    return user

# Gets chat by id
def get_chat(
        chat_id: str = Path(
            ...,
            min_length=1,
            title="Chat ID",
            description="Unique identifier of the chat",
        ),
        chat_repository: ChatRepository = Depends(get_chat_repository)

) -> ChatORM:

    # Asks Chat Repository to fetch result from DB
    chat = chat_repository.get_chat(chat_id)

    # Validation: If found then chat is returned, otherwise ChatNotFound exception
    if chat is None:
        raise ChatNotFoundError(chat_id)
    return chat

# Gets message by id
def get_message(
        message_id: str = Path(
            ...,
            min_length=1,
            title="Message ID",
            description="Unique identifier of the message",
            examples=["msg_001"]
        ),
        message_repository: MessageRepository = Depends(get_message_repository)

) -> MessageORM:

    # Asks Message Repository to fetch result from DB
    message = message_repository.get(message_id)

    # Validation: If found then message is returned, otherwise MessageNotFound exception
    if message is None:
        raise MessageNotFoundError(message_id)
    return message