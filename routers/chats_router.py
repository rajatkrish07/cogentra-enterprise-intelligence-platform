from starlette import status
from schemas import AddMessageRequest, EditMessageRequest, AddMessageResponse, EditMessageResponse, EditMsgResponse, \
    RenameChatRequest, RenameChatResponse, RenameChatDetail, DeleteMessageResponse, DeleteMessageDetail, AddMsgResponse
from fastapi import APIRouter, Path, Depends
from dependencies import get_chat, get_message, get_chat_service
from models import ChatORM, MessageORM
from services.chat_service import ChatService

# Initializing User Router
chat_router = APIRouter(
    prefix="/chats",
    tags=["chats"]
)

# Creating an instance of Chat Service
chat_service: ChatService = Depends(get_chat_service)

# Add Message
@chat_router.post("/{chat_id}/messages", response_model=AddMessageResponse, status_code=status.HTTP_201_CREATED)
def add_message(
    request: AddMessageRequest,
    chat_id: str = Path(
            ...,
            description="The id of the chat you are adding to.",
        ),
    chat: ChatORM = Depends(get_chat)
)->AddMessageResponse:

    msg = chat_service.add_message(
        chat = chat,
        text = request.text
    )

    return AddMessageResponse(
        message = "Message added successfully!",
        detail = AddMsgResponse(
            chat_id = chat_id,
            text = msg.text
        )
    )

@chat_router.patch("/{chat_id}/messages/{message_id}", response_model=EditMessageResponse, status_code= status.HTTP_200_OK)
def edit_message(
        request: EditMessageRequest,
        message: MessageORM = Depends(get_message)

) -> EditMessageResponse:

    msg = chat_service.edit_message(
        message = message,
        new_text = request.text
    )

    return EditMessageResponse(
        message = "Message edited successfully!",
        detail = EditMsgResponse(
            msg_id = msg.id,
            text = msg.text
    )
)

@chat_router.patch("/{chat_id}", response_model=RenameChatResponse, status_code=status.HTTP_200_OK)
def rename_chat(
        request: RenameChatRequest,
        chat: ChatORM = Depends(get_chat)
) -> RenameChatResponse:

    chat = chat_service.rename_chat(
        chat = chat,
        new_title = request.title
    )

    return RenameChatResponse(
        message = "Chat renamed successfully!",
        detail = RenameChatDetail(
            chat_id=chat.id,
            title=chat.title
        )
    )

@chat_router.delete("/{chat_id}/messages/{message_id}", response_model=DeleteMessageResponse, status_code=status.HTTP_200_OK)
def delete_message(
        chat: ChatORM = Depends(get_chat),
        message: MessageORM = Depends(get_message)
) -> DeleteMessageResponse:

    msg = chat_service.delete_message(
        chat = chat,
        message = message
    )

    return DeleteMessageResponse(
        message = "Message deleted successfully!",
        detail = DeleteMessageDetail(
            message_id = msg.id
        )
    )
