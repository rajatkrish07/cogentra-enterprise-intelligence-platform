from datetime import datetime
from fastapi import APIRouter, Depends
from models import Message
from dependencies import get_api_version, get_message
from schemas import GenerateAIResponse, RegenerateAIResponse, ResponseHistorySchema
from models import AIResponse
from starlette import status

from services import ai_service
from services.ai_service import AIService

message_router = APIRouter(
    prefix="/chats/{chat_id}/messages/{message_id}",
    tags=["Messages"]
)

# Generates the message
@message_router.post("/generate", response_model=GenerateAIResponse, status_code=status.HTTP_201_CREATED)
def create_ai_response(
    version: str = Depends(get_api_version),
    message: Message = Depends(get_message)
):

    return {
        "chat_id": message.chat_id,
        "message_id": message.id,
        "user_prompt": message.text,
        "ai_response": "Dependency Injection allows...",
        "version": version
    }

# Regenerates the response and adds it to a list for persistence

ai_service = AIService()

@message_router.post("/regenerate",response_model=RegenerateAIResponse, status_code=status.HTTP_201_CREATED)
def regenerate_response(
        message: Message = Depends(get_message)
):
    new_response = ai_service.regenerate_response(message)

    return {
        "message": "AI response regenerated successfully.",
        "response": new_response,
    }

# Displays all the responses generated
@message_router.get("/responses", response_model=ResponseHistorySchema, status_code=status.HTTP_200_OK)
def get_response_history(
        message: Message = Depends(get_message)
):

    return{
        "message": "Responses retrieved successfully.",
        "responses": message.responses
    }

