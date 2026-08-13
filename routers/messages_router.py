from starlette import status
from models import ChatORM, MessageORM
from schemas import AddMessageRequest, EditMessageRequest, AddMessageResponse, EditMessageResponse, EditMsgResponse, AddMsgResponse, DeleteMessageResponse, DeleteMessageDetail
from dependencies import get_chat, get_message, get_message_service
from fastapi import APIRouter, Path, Depends
from services.message_service import MessageService

# Message Router
messages_router = APIRouter(
    prefix="/chats",
    tags=["messages"]
)

# Create message endpoint
@messages_router.post("/{chat_id}/messages", response_model=AddMessageResponse, status_code=status.HTTP_201_CREATED)
def add_message(
    request: AddMessageRequest,
    chat_id: str = Path(
            ...,
            description="The id of the chat you are adding to."
        ),
    chat: ChatORM = Depends(get_chat),
    message_service: MessageService = Depends(get_message_service)
)->AddMessageResponse:

    msg = message_service.add_message(
        chat = chat,
        text = request.text
    )

    return AddMessageResponse(
        message = f"Message added successfully!",
        detail = AddMsgResponse(
            chat_id = chat_id,
            text = msg.text
        )
    )

@messages_router.patch("/messages/{message_id}", response_model=EditMessageResponse, status_code= status.HTTP_200_OK)
def edit_message(
        request: EditMessageRequest,
        message: MessageORM = Depends(get_message),
        message_service: MessageService = Depends(get_message_service)
) -> EditMessageResponse:

    msg = message_service.edit_message(
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

@messages_router.delete("/messages/{message_id}", response_model=DeleteMessageResponse, status_code=status.HTTP_200_OK)
def delete_message(
        message: MessageORM = Depends(get_message),
        message_service: MessageService = Depends(get_message_service)
) -> DeleteMessageResponse:

    msg = message_service.delete_message(
        message = message
    )

    return DeleteMessageResponse(
        message = "Message deleted successfully!",
        detail = DeleteMessageDetail(
            message_id = msg.id
        )
    )


