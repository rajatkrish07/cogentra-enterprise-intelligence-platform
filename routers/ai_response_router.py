from fastapi import APIRouter, Depends
from dependencies import get_api_version, get_ai_service, get_message
from models import MessageORM
from schemas import GenerateAIResponse, RegenerateAIResponse, ResponseHistorySchema, AIResponseSchema
from starlette import status
from services.ai_response_service import AIService

ai_response_router = APIRouter(
    prefix="/messages",
    tags=["AI Responses"]
)

# Generates the message
@ai_response_router.post("/{message_id}/ai/responses/generate", response_model=GenerateAIResponse, status_code=status.HTTP_201_CREATED)
def generate_response(
    version: str = Depends(get_api_version),
    ai_service: AIService = Depends(get_ai_service),
    message: MessageORM = Depends(get_message)
)->GenerateAIResponse:

    response = ai_service.generate_response(message)

    return GenerateAIResponse(
        ai_response = response.text,
        version = version
    )

# Regenerates the response and adds it to a list for persistence
@ai_response_router.post("/{message_id}/ai/responses/regenerate",response_model=RegenerateAIResponse, status_code=status.HTTP_201_CREATED)
def regenerate_response(
        ai_service: AIService = Depends(get_ai_service),
        message: MessageORM = Depends(get_message)
) -> RegenerateAIResponse:

    new_response = ai_service.regenerate_response(message)

    return RegenerateAIResponse(
        message = "AI response regenerated successfully.",
        response = AIResponseSchema(
            id = new_response.id,
            text = new_response.text,
            created_at = new_response.created_at
        )
)

# Displays all the responses generated
@ai_response_router.get("/{message_id}/ai/responses", response_model=ResponseHistorySchema, status_code=status.HTTP_200_OK)
def response_history(
        ai_service: AIService = Depends(get_ai_service),
        message: MessageORM = Depends(get_message)
)->ResponseHistorySchema:

    responses = ai_service.response_history(message)

    return ResponseHistorySchema(
        message = "Responses retrieved successfully.",
        responses = [
            AIResponseSchema(
                id = response.id,
                text = response.text,
                created_at=response.created_at
            )
            for response in responses
        ]
    )

