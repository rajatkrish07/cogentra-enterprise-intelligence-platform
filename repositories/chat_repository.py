from sqlalchemy import select
from models import ChatORM

class ChatRepository:
    def __init__(self, db):
        self.db = db

    def get_chat(self, chat_id: str) -> ChatORM | None:
        stmt = select(ChatORM).where(ChatORM.id == chat_id)
        execute = self.db.execute(stmt)
        result = execute.scalars().first()
        return result

    def update(self, chat: ChatORM):
        self.db.add(chat)
        self.db.commit()
        return chat