from datetime import datetime
from schemas import CurrentUser
from models import Chat, Message
from fastapi import Depends, Path
from fastapi import HTTPException
from starlette import status

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
                        timestamp=datetime.now(),
                        text="What is Python?"
                        ),
                    Message(
                        id="msg_002",
                        timestamp=datetime.now(),
                        text="Explain OOP."
                    )
                ]
            ),

            Chat(
                id="chat_002",
                title="FastAPI",
                messages=[
                    Message(
                        id="msg_003",
                        timestamp=datetime.now(),
                        text="What is Dependency Injection?"
                    ),
                    Message(
                        id="msg_004",
                        timestamp=datetime.now(),
                        text="Explain Path Parameters."
                    )
                ]
            ),

            Chat(
                id="chat_003",
                 title="RAG",
                 messages=[
                     Message(
                         id="msg_005",
                         timestamp=datetime.now(),
                         text="What is Retrieval-Augmented Generation?"
                     ),
                     Message(
                         id="msg_006",
                         timestamp=datetime.now(),
                         text="Explain Vector Databases."
                     ),
                 ]
            ),

            Chat(
                id="chat_004",
                 title="Agents",
                 messages=[
                     Message(
                         id="msg_007",
                         timestamp=datetime.now(),
                         text="What are AI Agents?"
                     ),
                     Message(
                         id="msg_008",
                         timestamp=datetime.now(),
                         text="Explain Agentic Workflows."
                     ),
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

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Chat ID with '{chat_id}' is not found."
    )

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

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Message with '{message_id}' is not found."
    )

