from pydantic import BaseModel, EmailStr, Field


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

# Response Model

class AIResponse(BaseModel):
    message_id: int
    chat_id: int
    user_prompt: str
    ai_response: str

