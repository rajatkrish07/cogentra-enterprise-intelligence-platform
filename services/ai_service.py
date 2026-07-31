from datetime import datetime
from models import Message, AIResponse

class AIService:

    def generate_response(
            self,
            message: Message
    )->AIResponse:

        response = AIResponse(
            id="resp_009",
            text="This is a generated AI response.",
            created_at=datetime.now()
        )

        message.responses.append(response)

        return response

    def regenerate_response(
            self,
            message: Message
    )->AIResponse:

        new_response = AIResponse(
            id="resp_009",
            text="This is a regenerated AI response.",
            created_at=datetime.now()
        )

        message.responses.append(new_response)

        return new_response

    def response_history(
            self,
            message: Message
    )->list[AIResponse]:

        return message.responses

