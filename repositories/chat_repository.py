from sqlalchemy import select
from models import ChatORM

class ChatRepository:
    def __init__(self, db):
        self.db = db

    # Fetches chat by ID
    def get_chat(self, chat_id: str) -> ChatORM | None:
        stmt = select(ChatORM).where(ChatORM.id == chat_id)
        execute = self.db.execute(stmt)
        result = execute.scalars().first()
        return result

    # Fetches chat by title
    def get_chat_by_title(self, user_id: str, title: str) -> ChatORM | None:
        stmt = select(ChatORM).where(
            ChatORM.id == user_id,
            ChatORM.title == title
        )
        execute = self.db.execute(stmt)
        result = execute.scalars().first()
        return result

    def create(self, chat: ChatORM) -> ChatORM:
        self.db.add(chat)
        self.db.commit()
        return chat

    # Renames/Updates chat title or name
    def update(self, chat: ChatORM) -> ChatORM:
        self.db.add(chat)
        self.db.commit()
        return chat

    def delete(self, chat: ChatORM) -> ChatORM:
        self.db.delete(chat)
        self.db.commit()
        return chat