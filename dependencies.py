from datetime import datetime
# from schemas import CurrentUser
from models import ChatORM, MessageORM
from exceptions import ChatNotFoundError, MessageNotFoundError
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

# # Validates Current User
# def get_curr_user() -> CurrentUser:
#     return CurrentUser(
#         username="rajatkr_07",
#         email="rajatkrishnan2002@gmail.com",
#         chats=[
#             ChatORM(
#                 id="chat_001",
#                 title="Python",
#                 messages=[
#                     MessageORM(
#                         id="msg_001",
#                         chat_id="chat_001",
#                         timestamp=datetime.now(),
#                         text="What is Python?",
#                     ),
#
#                     MessageORM(
#                         id="msg_002",
#                         chat_id="chat_001",
#                         timestamp=datetime.now(),
#                         text="Explain OOP.",
#                     )
#                 ]
#             ),
#
#             ChatORM(
#                 id="chat_002",
#                 title="FastAPI",
#                 messages=[
#
#                     MessageORM(
#                         id="msg_003",
#                         chat_id="chat_002",
#                         timestamp=datetime.now(),
#                         text="What is Dependency Injection?",
#                     ),
#
#                     MessageORM(
#                         id="msg_004",
#                         chat_id="chat_002",
#                         timestamp=datetime.now(),
#                         text="Explain Path Parameters.",
#                     )
#                 ]
#             ),
#
#             ChatORM(
#                 id="chat_003",
#                  title="RAG",
#                  messages=[
#                      MessageORM(
#                          id="msg_005",
#                          chat_id="chat_003",
#                          timestamp=datetime.now(),
#                          text="What is Retrieval-Augmented Generation?"
#                      ),
#
#                      MessageORM(
#                          id="msg_006",
#                          chat_id="chat_003",
#                          timestamp=datetime.now(),
#                          text="Explain Vector Databases."
#                      )
#                  ]
#             ),
#
#             ChatORM(
#                 id="chat_004",
#                 title="Agents",
#                 messages=[
#
#                      MessageORM(
#                          id="msg_007",
#                          chat_id="chat_004",
#                          timestamp=datetime.now(),
#                          text="What are AI Agents?"
#                      ),
#
#                      MessageORM(
#                          id="msg_008",
#                          chat_id="chat_004",
#                          timestamp=datetime.now(),
#                          text="Explain Agentic Workflows.",
#                      )
#                  ]
#             ),
#         ]
#     )

# Gets chat by id
def get_chat(
        chat_id: str = Path(
            ...,
            min_length=1,
            title="Chat ID",
            description="Unique identifier of the chat",
            examples=["chat_001"]
        ),
        chat_repository: ChatRepository = Depends(get_chat_repository)

) -> ChatORM:

    # Asks Chat Repository to fetch result from DB
    chat = chat_repository.get_chat(chat_id)

    # Validation: If found then chat is returned, otherwise None
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

    # Validation: If found then message is returned, otherwise None
    if message is None:
        raise MessageNotFoundError(message_id)
    return message