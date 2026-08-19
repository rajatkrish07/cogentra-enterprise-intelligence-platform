from models import AIResponseORM
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

class AIResponseRepository:

    def __init__(self, db):
        self.db = db

    # Persists the AI generated response
    def create(self, response: AIResponseORM):
        try:
            self.db.add(response)
            self.db.commit()

        except IntegrityError:
            self.db.rollback()
            raise
        return response

    # Fetches all the responses
    def get_all(self):
        stmt = select(AIResponseORM)
        execute = self.db.execute(stmt)
        results = execute.scalars().all()
        return results

    # Fetches response by id
    def get_by_id(self, response_id: str):
        stmt = select(AIResponseORM).where(
            AIResponseORM.id == response_id
        )
        execute = self.db.execute(stmt)
        result = execute.scalars().one()
        return result

    # Fetches response by id
    def get_by_message_id(
            self,
            message_id: str
    ) -> list[AIResponseORM]:

        stmt = select(AIResponseORM).where(
            AIResponseORM.message_id == message_id
        ).order_by(AIResponseORM.created_at.desc())

        execute = self.db.execute(stmt)
        result = execute.scalars().all()
        return result