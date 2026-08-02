from starlette import status
from schemas import CreateChatRequest, CreateChatResponse, ChatResponse, DeleteChatResponse, UpdateEmailResponse, UpdateEmailRequest
from fastapi import APIRouter, Path
from fastapi.params import Depends
from dependencies import get_curr_user
from models import UserAccount
from services import user_service
from services.user_service import UserService

# Initializing User Router
user_router = APIRouter(
    prefix="/users",
    tags=["users"]
)

# Creating an instance of User Service
user_service = UserService()

# Create Chat
@user_router.post("/{user_id}/chats", response_model=CreateChatResponse, status_code=status.HTTP_201_CREATED)

def create_chat(
        request: CreateChatRequest,
        user: UserAccount = Depends(get_curr_user)

) -> CreateChatResponse:

    chat = user_service.create_chat(
        user = user,
        title = request.title
    )

    return CreateChatResponse(
        message= "Chat created successfully!",
        chat= ChatResponse(
            id=chat.id,
            title=chat.title,
        )
)

# Delete Chat
@user_router.delete("/{user_id}/chats/{chat_id}", response_model=DeleteChatResponse, status_code=status.HTTP_200_OK)

def delete_chat(
        chat_id: str = Path(
            ...,
            description="The id of the chat to delete",
        ),
        user: UserAccount = Depends(get_curr_user)
) -> DeleteChatResponse:

    chat = user_service.delete_chat(
        user = user,
        chat_id = chat_id
    )

    return DeleteChatResponse(
        message= "Chat deleted successfully!",
        chat= ChatResponse(
            id=chat.id,
            title=chat.title,
        )
    )

# Updates user email
@user_router.patch("/{user_id}/email", response_model=UpdateEmailResponse, status_code=status.HTTP_200_OK)
def update_email(
        request: UpdateEmailRequest,
        user: UserAccount = Depends(get_curr_user),
) -> UpdateEmailResponse:

    user_service.update_email(
        user = user,
        new_email = request.new_email
    )

    return UpdateEmailResponse(
        message= "Email updated successfully!",
        email= user.email
    )





