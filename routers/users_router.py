from starlette import status
from models import UserORM
from schemas import UpdateEmailResponse, UpdateEmailRequest, UpdateEmailDetail, UserResponse, UserRequest, \
    UserResponseDetail
from fastapi import APIRouter
from fastapi.params import Depends
from dependencies import get_user, get_user_service
from services.user_service import UserService

# Initializing User Router
user_router = APIRouter(
    prefix="/users",
    tags=["users"]
)

# Create user request
@user_router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
        request: UserRequest,
        user_service: UserService = Depends(get_user_service)
):
    user = UserORM(
        username = request.username,
        email = request.email,
        first_name = request.first_name,
        last_name = request.last_name
    )

    # Asks Service layer to handle the logic
    created_user = user_service.create_user(user)

    # Returns the JSON response back to the client
    return UserResponse(
        message = f"User {created_user.username} created successfully!",
        detail = UserResponseDetail(
            username = created_user.username,
            email = created_user.email
        )
    )

# Update user email request
@user_router.patch("/{user_id}/email", response_model=UpdateEmailResponse, status_code=status.HTTP_200_OK)
def update_email(
        request: UpdateEmailRequest,
        user: UserORM = Depends(get_user),
        user_service: UserService = Depends(get_user_service)
) -> UpdateEmailResponse:

    user = user_service.update_email(
        user = user,
        new_email = request.new_email
    )

    return UpdateEmailResponse(
        message= "Email updated successfully!",
        detail = UpdateEmailDetail(
            username=user.username,
            email=user.email
        )
    )
