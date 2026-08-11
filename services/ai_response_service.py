from uuid import uuid4
from datetime import datetime
from models import AIResponseORM
from repositories.ai_response_repository import AIResponseRepository

class AIService:

    def __init__(self, repository: AIResponseRepository):
        self.repository = repository

# Generates response
    def generate_response(
            self
    )->AIResponseORM:

        response = AIResponseORM(
            id=str(uuid4()),
            message_id=str(uuid4()),
            text="This is a generated AI response.",
            created_at=datetime.now()
        )

        self.repository.create(response)
        return response

# Regenerates response
    def regenerate_response(
            self
    )->AIResponseORM:

        new_response = AIResponseORM(
            id=str(uuid4()),
            message_id=str(uuid4()),
            text="This is a regenerated AI response.",
            created_at=datetime.now()
        )

        self.repository.create(new_response)
        return new_response

# Returns response history
    def response_history(
            self,
    )->list[AIResponseORM]:

        return self.repository.get_all()

