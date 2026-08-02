from datetime import datetime
from pydantic import BaseModel, EmailStr, Field
from models import Chat

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

class GenerateAIResponse(BaseModel):
    chat_id: str
    message_id: str
    user_prompt: str
    ai_response: str
    version: str

class AIResponseSchema(BaseModel):
    id: str
    text: str
    created_at: datetime

class RegenerateAIResponse(BaseModel):
    message: str
    response: AIResponseSchema


class ResponseHistorySchema(BaseModel):
    message: str
    responses: list[AIResponseSchema]


class UserRegistrationRequest(BaseModel):
    username: str
    email: EmailStr


class CreateChatRequest(BaseModel):
    title: str


class ChatResponse(BaseModel):
    id: str
    title: str


class CreateChatResponse(BaseModel):
    message: str
    chat: ChatResponse


class DeleteChatResponse(BaseModel):
    message: str
    chat: ChatResponse
