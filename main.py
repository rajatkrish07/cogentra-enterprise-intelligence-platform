from click import prompt

from models import UserAccount
from schemas import UserResponse, AdminUserResponse, AIUserResponse ,AIResponse, GenerateResponseRequest
from fastapi import FastAPI, Query, Path, Header
from starlette import status

# app -> FastAPI Application object
app = FastAPI()

@app.post("/admin/users", response_model=AdminUserResponse)
def admin_display(user: UserAccount):
    return user

@app.post("/users", response_model=UserResponse)
def user_display(user: UserAccount):
    return user

@app.post("/ai/users", response_model=AIUserResponse)
def ai_display(user: UserAccount):
    return user

# Welcome page
@app.get("/")
def welcome_user():
    return {"message": "Welcome User!"}

# App's health check
@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "cogentra"
    }

# Path Parameter

# Fetching user info by id

@app.get("/users/{user_id}")
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
@app.get("/users")
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
@app.get("/profile")
def profile(
        authorization: str = Header(
            ...,
            description="JWT Bearer Token"
        )
):
    return {
        "token": authorization
    }


# Endpoint and Logic

@app.post("/chats/{chat_id}/generate", response_model=AIResponse, status_code=status.HTTP_201_CREATED)
def create_ai_response(
    request: GenerateResponseRequest,
    chat_id: int = Path(
            ...,
            ge=1,
            title="Chat ID",
            description="Unique identifier of the chat"
        ),
):
    return {
        "message_id": 201,
        "chat_id": chat_id,
        "user_prompt": request.prompt,
        "ai_response": "Dependency Injection allows..."
    }
