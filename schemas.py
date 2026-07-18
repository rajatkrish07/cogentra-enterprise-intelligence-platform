from pydantic import BaseModel, EmailStr, Field
from models import Chat, Message

# Exposes fields relevant for admin only
class UserResponse(BaseModel):
    username: str
    full_name: str

class AdminUserResponse(BaseModel):
    username: str
    email: EmailStr
    chat_count: int

class AIUserResponse(BaseModel):
    username: str
    chat_count: int

# Request Model:

class GenerateResponseRequest(BaseModel):
    prompt: str = Field(
        ...,
        min_length=5,
        max_length=4000,
        description="User prompt sent to Cogentra AI",
        examples=["Explain FastAPI Dependency Injection."]
    )

class CurrentUser(BaseModel):
    username: str
    email: EmailStr
    chats: list[Chat]

# Response Model

class AIResponse(BaseModel):
    chat_id: str
    message_id: str
    user_prompt: str
    ai_response: str
    version: str
    username: str
    email: EmailStr



