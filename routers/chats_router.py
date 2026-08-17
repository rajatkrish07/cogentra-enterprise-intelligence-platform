from starlette import status
from schemas import RenameChatRequest, RenameChatResponse, RenameChatDetail, CreateChatResponse, CreateChatRequest, ChatResponseDetail
from fastapi import APIRouter, Depends
from dependencies import get_chat, get_chat_service
from models import ChatORM, UserORM
from services.chat_service import ChatService

# Initializing User Router
chat_router = APIRouter(
    prefix="/chats",
    tags=["chats"]
)

@chat_router.post("/chats", response_model=CreateChatResponse, status_code=status.HTTP_201_CREATED)
def create_chat(
        request: CreateChatRequest,
        user_id: str,
        chat_service: ChatService = Depends(get_chat_service)
):
    chat = chat_service.create_chat(
        user_id = user_id,
        title = request.title
    )

    return CreateChatResponse(
        message = "Chat created successfully!",
        detail = ChatResponseDetail(
            id = chat.id,
            title = chat.title
        )
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