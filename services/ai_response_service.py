from uuid import uuid4
from datetime import datetime
from models import AIResponseORM, MessageORM
from repositories.ai_response_repository import AIResponseRepository

class AIService:

    def __init__(self, ai_response_repository: AIResponseRepository):
        self.ai_response_repository = ai_response_repository

# Generates response
    def generate_response(
            self,
            message: MessageORM,
    )->AIResponseORM:

        response = AIResponseORM(
            id=str(uuid4()),
            message_id=message.id,
            text="This is a generated AI response.",
            created_at=datetime.now()
        )

        self.ai_response_repository.create(response)
        return response

# Regenerates response
    def regenerate_response(
            self,
            message: MessageORM,
    )->AIResponseORM:

        new_response = AIResponseORM(
            id=str(uuid4()),
            message_id=message.id,
            text="This is a regenerated AI response.",
            created_at=datetime.now()
        )

        self.ai_response_repository.create(new_response)
        return new_response

# Returns response history
    def response_history(
            self,
    )->list[AIResponseORM]:

        return self.ai_response_repository.get_all()

