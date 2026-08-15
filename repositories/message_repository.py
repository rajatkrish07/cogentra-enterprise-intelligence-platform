from models import MessageORM
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

class MessageRepository:
    def __init__(self, db):
        self.db = db

    def get(self, message_id: str) -> MessageORM | None:
        stmt = select(MessageORM).where(MessageORM.id == message_id)
        execute = self.db.execute(stmt)
        result = execute.scalars().first()
        return result

    def get_by_chat_id(self, chat_id: str) -> MessageORM | None:
        stmt = select(MessageORM).where(MessageORM.chat_id == chat_id)
        execute = self.db.execute(stmt)
        result = execute.scalars().first()
        return result

    def create(self, message: MessageORM):
        try:
            self.db.add(message)
            self.db.commit()

        except IntegrityError:
            self.db.rollback()
            raise

        return message

    def update(self, message: MessageORM):
        self.db.add(message)
        self.db.commit()
        return message

    def delete(self, message: MessageORM):
        self.db.delete(message)
        self.db.commit()
        return message
