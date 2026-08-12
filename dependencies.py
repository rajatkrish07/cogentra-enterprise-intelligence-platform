from datetime import datetime
from schemas import CurrentUser
from models import Chat, Message
from exceptions import ChatNotFoundError, MessageNotFoundError
from fastapi import Depends, Path
from database.database import SessionLocal
from services.ai_response_service import AIService
from services.chat_service import ChatService
from repositories.ai_response_repository import AIResponseRepository
from repositories.chat_repository import ChatRepository
from repositories.message_repository import MessageRepository

# Returns API Version
def get_api_version() -> str:
    return "v1"

# Validates Current User
def get_curr_user() -> CurrentUser:
    return CurrentUser(
        username="rajatkr_07",
        email="rajatkrishnan2002@gmail.com",
        chats=[
            Chat(
                id="chat_001",
                title="Python",
                messages=[
                    Message(
                        id="msg_001",
                        chat_id="chat_001",
                        timestamp=datetime.now(),
                        text="What is Python?",
                    ),

                    Message(
                        id="msg_002",
                        chat_id="chat_001",
                        timestamp=datetime.now(),
                        text="Explain OOP.",
                    )
                ]
            ),

            Chat(
                id="chat_002",
                title="FastAPI",
                messages=[

                    Message(
                        id="msg_003",
                        chat_id="chat_002",
                        timestamp=datetime.now(),
                        text="What is Dependency Injection?",
                    ),

                    Message(
                        id="msg_004",
                        chat_id="chat_002",
                        timestamp=datetime.now(),
                        text="Explain Path Parameters.",
                    )
                ]
            ),

            Chat(
                id="chat_003",
                 title="RAG",
                 messages=[
                     Message(
                         id="msg_005",
                         chat_id="chat_003",
                         timestamp=datetime.now(),
                         text="What is Retrieval-Augmented Generation?"
                     ),

                     Message(
                         id="msg_006",
                         chat_id="chat_003",
                         timestamp=datetime.now(),
                         text="Explain Vector Databases."
                     )
                 ]
            ),

            Chat(
                id="chat_004",
                title="Agents",
                messages=[

                     Message(
                         id="msg_007",
                         chat_id="chat_004",
                         timestamp=datetime.now(),
                         text="What are AI Agents?"
                     ),

                     Message(
                         id="msg_008",
                         chat_id="chat_004",
                         timestamp=datetime.now(),
                         text="Explain Agentic Workflows.",
                     )
                 ]
            ),
        ]
    )

def get_chat(
        chat_id: str = Path(
            ...,
            min_length=1,
            title="Chat ID",
            description="Unique identifier of the chat",
            examples=["chat_001"]
        ),
        curr_user: CurrentUser = Depends(get_curr_user)

) -> Chat:

    for chat in curr_user.chats:
        if chat.id == chat_id:
            return chat

    raise ChatNotFoundError(chat_id)

def get_message(
        message_id: str = Path(
            ...,
            min_length=1,
            title="Message ID",
            description="Unique identifier of the message",
            examples=["msg_001"]
        ),
        chat: Chat = Depends(get_chat)

) -> Message:

    for message in chat.messages:
        if message.id == message_id:
            return message

    raise MessageNotFoundError(message_id)

# Repository dependency

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

def get_ai_response_repository(
        db = Depends(get_db)
):
    return AIResponseRepository(db)

def get_ai_service(
        repository: AIResponseRepository = Depends(get_ai_response_repository)
)-> AIService:
    return AIService(repository)

def get_chat_repository(
        db = Depends(get_db)
):
    return ChatRepository(db)

def get_message_repository(
        db = Depends(get_db)
):
    return MessageRepository(db)

def get_chat_service(
        chat_repository: ChatRepository = Depends(get_chat_repository),
        message_repository: MessageRepository = Depends(get_message_repository)
) -> ChatService:
    return ChatService(chat_repository, message_repository)
