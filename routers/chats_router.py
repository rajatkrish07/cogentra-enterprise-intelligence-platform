from starlette import status
from schemas import RenameChatRequest, RenameChatResponse, RenameChatDetail
from fastapi import APIRouter, Depends
from dependencies import get_chat, get_chat_service
from models import ChatORM
from services.chat_service import ChatService

# Initializing User Router
chat_router = APIRouter(
    prefix="/chats",
    tags=["chats"]
)

# Renames Chat name/title
@chat_router.patch("/{chat_id}", response_model=RenameChatResponse, status_code=status.HTTP_200_OK)
def rename_chat(
        request: RenameChatRequest,
        chat: ChatORM = Depends(get_chat),
        chat_service: ChatService = Depends(get_chat_service)

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