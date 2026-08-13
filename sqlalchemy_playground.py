import uuid
from datetime import datetime
from database.database import SessionLocal
from models import UserORM, ChatORM, MessageORM, Message
from repositories.chat_repository import ChatRepository
from repositories.message_repository import MessageRepository
from services.chat_service import ChatService


# Database Session
db = SessionLocal()


# Create test user
user = UserORM(
    id=str(uuid.uuid4()),
    username=f"test_user_{uuid.uuid4().hex[:8]}",
    email=f"test_{uuid.uuid4().hex[:8]}@example.com",
    first_name="Test",
    last_name="User"
)

db.add(user)
db.commit()


# Create test chat
chat = ChatORM(
    id=str(uuid.uuid4()),
    user_id=user.id,
    title="Test Chat"
)

db.add(chat)
db.commit()

message = MessageORM(
    id=str(uuid.uuid4()),
    chat_id=chat.id,
    timestamp=datetime.now(),
    text="Test Message"
)

db.add(message)
db.commit()

# Initialize repositories
chat_repo = ChatRepository(db)
message_repo = MessageRepository(db)


# Initialize service
chat_service = ChatService(
    chat_repo,
    message_repo
)

# Test Chat retrieval
chat_from_db = chat_repo.get_chat(chat.id)
print("Chat:", chat_from_db.id)
print("Title:", chat_from_db.title)

# Test Message retrieval
message_from_db = message_repo.get(message.id)
print("Message:", message_from_db.id)
print("Text:", message_from_db.text)

# Repository Not Found Contract
missing_message = message_repo.get("does-not-exist")
print("Missing message:", missing_message)