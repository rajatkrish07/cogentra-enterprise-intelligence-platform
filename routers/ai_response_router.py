from fastapi import APIRouter, Depends
from dependencies import get_api_version, get_ai_service
from schemas import GenerateAIResponse, RegenerateAIResponse, ResponseHistorySchema
from starlette import status
from services.ai_response_service import AIService

ai_response_router = APIRouter(
    prefix="/ai/responses",
    tags=["AI Responses"]
)

# Generates the message
@ai_response_router.post("/generate", response_model=GenerateAIResponse, status_code=status.HTTP_201_CREATED)
def generate_response(
    version: str = Depends(get_api_version),
    ai_service: AIService = Depends(get_ai_service)
):

    response = ai_service.generate_response()

    return {
        "ai_response": response.text,
        "version": version
    }

# Regenerates the response and adds it to a list for persistence
@ai_response_router.post("/regenerate",response_model=RegenerateAIResponse, status_code=status.HTTP_201_CREATED)
def regenerate_response(
        ai_service: AIService = Depends(get_ai_service)
):
    new_response = ai_service.regenerate_response()

    return {
        "message": "AI response regenerated successfully.",
        "response": new_response,
    }

# Displays all the responses generated
@ai_response_router.get("/responses", response_model=ResponseHistorySchema, status_code=status.HTTP_200_OK)
def response_history(
        ai_service: AIService = Depends(get_ai_service)
):

    resp_history = ai_service.response_history()

    return{
        "message": "Responses retrieved successfully.",
        "responses": resp_history
    }

