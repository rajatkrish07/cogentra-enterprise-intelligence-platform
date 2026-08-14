from datetime import datetime
from pydantic import BaseModel, EmailStr, Field

class UserRequest(BaseModel):
    username: str
    email: EmailStr
    first_name: str
    last_name: str

class UserResponseDetail(BaseModel):
    username: str
    email: EmailStr

class UserResponse(BaseModel):
    message: str
    detail: UserResponseDetail

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

class GenerateAIResponse(BaseModel):
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

class DeleteChatRequest(BaseModel):
    id: str

class DeleteChatResponse(BaseModel):
    message: str
    chat: ChatResponse

class UpdateEmailRequest(BaseModel):
    new_email: EmailStr

class UpdateEmailDetail(BaseModel):
    username: str
    email: EmailStr

class UpdateEmailResponse(BaseModel):
    message: str
    detail: UpdateEmailDetail

class AddMessageRequest(BaseModel):
    text: str

class AddMsgResponse(BaseModel):
    chat_id: str
    text: str

class AddMessageResponse(BaseModel):
    message: str
    detail: AddMsgResponse

class EditMessageRequest(BaseModel):
    text: str

class EditMsgResponse(BaseModel):
    msg_id: str
    text: str

class EditMessageResponse(BaseModel):
    message: str
    detail: EditMsgResponse

class RenameChatRequest(BaseModel):
    title: str

class RenameChatDetail(BaseModel):
    chat_id: str
    title: str

class RenameChatResponse(BaseModel):
    message: str
    detail: RenameChatDetail

class DeleteMessageDetail(BaseModel):
    message_id: str

class DeleteMessageResponse(BaseModel):
    message: str
    detail: DeleteMessageDetail