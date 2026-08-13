from starlette import status
from schemas import UpdateEmailResponse, UpdateEmailRequest, UpdateEmailDetail
from fastapi import APIRouter
from fastapi.params import Depends
from dependencies import get_user_service
from services.user_service import UserService

# Initializing User Router
user_router = APIRouter(
    prefix="/users",
    tags=["users"]
)

# Updates user email
@user_router.patch("/{user_id}/email", response_model=UpdateEmailResponse, status_code=status.HTTP_200_OK)
def update_email(
        request: UpdateEmailRequest,
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
