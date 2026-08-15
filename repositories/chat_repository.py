from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from models import UserORM, ChatORM

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
            ChatORM.user_id == user_id,
            ChatORM.title == title
        )
        execute = self.db.execute(stmt)
        result = execute.scalars().first()
        return result

    # Persists newly created chat
    def create(self, chat: ChatORM) -> ChatORM:
        try:
            self.db.add(chat)
            self.db.commit()

        except IntegrityError:
            self.db.rollback()
            raise

        return chat

    # Persists updated email
    def update(self, chat: ChatORM) -> ChatORM:
        self.db.add(chat)
        self.db.commit()
        return chat

    def delete(self, chat: ChatORM) -> ChatORM:
        self.db.delete(chat)
        self.db.commit()
        return chat