from models import ChatORM

class ChatRepository:
    def __init__(self, db):
        self.db = db

    def update(self, chat: ChatORM):
        self.db.add(chat)
        self.db.commit()
        return chat