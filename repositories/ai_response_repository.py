from models import AIResponseORM
from sqlalchemy import select

class AIResponseRepository:

    def __init__(self, db):
        self.db = db

    def create(self, response: AIResponseORM):
        self.db.add(response)
        self.db.commit()
        return response


    def get_all(self):
        stmt = select(AIResponseORM)
        execute = self.db.execute(stmt)
        results = execute.scalars().all()
        return results

    def get_by_id(self, response_id: str):
        stmt = select(AIResponseORM).where(
            AIResponseORM.id == response_id
        )
        execute = self.db.execute(stmt)
        result = execute.scalars().one()
        return result