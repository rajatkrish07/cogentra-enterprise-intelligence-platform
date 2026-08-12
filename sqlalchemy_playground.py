import os
import uuid
from datetime import datetime
from database.database import SessionLocal
from models import UserORM, ChatORM, MessageORM, AIResponseORM
from sqlalchemy import select, or_

from repositories.ai_response_repository import AIResponseRepository
from services.ai_response_service import AIService
from services.chat_service import ChatService
from repositories.chat_repository import ChatRepository
from repositories.message_repository import MessageRepository


# Database Test Section
db = SessionLocal()

# Python objects (Table Entries)

ai_response = AIResponseORM(
    id="play_001",
    message_id=str(uuid.uuid4()),
    text="Hello From SQLAlchemy",
    created_at=datetime.now()
)

db.add(ai_response)
db.commit()

# Commits changes to the database
# db.commit()
#
# # Reading values frm the db as python objects (Similar to SELECT * FROM AIResponseORM)
# stmt = select(AIResponseORM)
# execute = db.execute(stmt)
# results=execute.scalars().all()
#
# for result in results:
#     print(result.id, result.text)
#
# # Reading values frm the db as python objects (Similar to SELECT * FROM AIResponseORM WHERE id = "play007")
# stmt = select(AIResponseORM).where(
#     AIResponseORM.id == "play_007",
# )
# execute = db.execute(stmt)
# result = execute.scalars().one()
# print(result.id, result.text)
#
# # Multiple WHERE conditions
# stmt = select(AIResponseORM).where(
#     AIResponseORM.id == "play_007",
#     AIResponseORM.text == "This is response seven"
# )
#
# execute = db.execute(stmt)
# result = execute.scalars().one()
# print(result.id, result.text)
#
# # OR Condition
# stmt = select(AIResponseORM).where(
#     or_(
#         AIResponseORM.id == "play_007",
#         AIResponseORM.id == "play_008"
#     )
# )
#
# execute = db.execute(stmt)
# results = execute.scalars().all()
#
# for result in results:
#     print(result.id, result.text)

user = UserORM(
    id=str(uuid.uuid4()),
    username="test_user",
    email="test@example.com",
    first_name="Test",
    last_name="User"
)

print("Before add:", user)
# db.add(user)

print("Before commit:", user)
db.commit()

print("After commit:", user)

users = db.query(UserORM).all()
print("Users in DB: ",users)


chat = ChatORM(
    id=str(uuid.uuid4()),
    user_id=user.id,
    title="Test Chat"
)

db.add(chat)
db.commit()

chat_repo = ChatRepository(db)
message_repo = MessageRepository(db)

chat_service = ChatService(
    chat_repo,
    message_repo
)

message = chat_service.add_message(
    chat = chat,
    text = "Testing MessageORM persistence.",
)

edited_message = chat_service.edit_message(
    message=message,
    new_text="Updated message text."
)
#
# delete_message = chat_service.delete_message(
#     message=edited_message,
# )
#
# remaining_messages = db.query(MessageORM).all()
#
# for msg in remaining_messages:
#     print(msg.id, msg.text)
#
# deleted = db.get(MessageORM, delete_message.id)
#
# print("Deleted message:", deleted)

renamed_chat = chat_service.rename_chat(
    chat = chat,
    new_title="New title"
)

print("CHAT OBJECT ID:", chat.id)
print("RENAMED OBJECT ID:", renamed_chat.id)
print("RENAMED TITLE:", renamed_chat.title)

saved_chat = db.get(ChatORM, renamed_chat.id)

print("SAVED CHAT:", saved_chat)

new_db = SessionLocal()

saved_chat = new_db.get(ChatORM, chat.id)

print("Fresh session title:", saved_chat.title)

new_db.close()