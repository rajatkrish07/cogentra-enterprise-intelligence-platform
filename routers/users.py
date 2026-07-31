from fastapi import APIRouter, Path, Query, Header, BackgroundTasks
from pydantic import EmailStr
from models import UserAccount
from schemas import UserResponse, UserRegistrationRequest
from logger import logger

user_router = APIRouter(
    prefix="/users",
    tags=["users"]
)

# Displays User/Client related fields only
@user_router.get("/", response_model=UserResponse)
def user_display(user: UserAccount):
    return user

# Fetching user info by id
@user_router.get("/{user_id}")
def get_user(
        user_id: int = Path(
            ...,
            ge=1,
            title="User ID",
            description="Unique identifier of the user",
            examples=[1]
        )
):
    return {
        "requested_user": user_id
    }

# Fetching user info by name
@user_router.get("/search")
def search_users(
        name: str | None= Query(
            None,
            title="User Name",
            min_length=2,
            max_length=50,
            description="Search users by username",
        )):
    return {
        "searched_name": name
    }

# Header param
@user_router.get("/profile")
def profile(
        authorization: str = Header(
            ...,
            description="JWT Bearer Token"
        )
):
    return {
        "token": authorization
    }

# Sends Welcome Email
def send_welcome_email(email: EmailStr):
    logger.info(f"Sending welcome email to {email}")

@user_router.post("/register")
async def register_user(
        user: UserRegistrationRequest,
        background_tasks: BackgroundTasks
):

    logger.info(f"Sending welcome email to {user.email}")

    background_tasks.add_task(
        task = send_welcome_email,
        email = user.email
    )
    return {
        "message": "User successfully registered"
    }