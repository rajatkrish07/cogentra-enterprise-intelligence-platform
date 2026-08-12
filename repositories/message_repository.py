from models import MessageORM

class MessageRepository:
    def __init__(self, db):
        self.db = db

    def create(self, message: MessageORM):
        self.db.add(message)
        self.db.commit()
        return message

    def update(self, message: MessageORM):
        self.db.add(message)
        self.db.commit()
        return message

    def delete(self, message: MessageORM):
        self.db.delete(message)
        self.db.commit()
        return message
