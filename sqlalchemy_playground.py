from datetime import datetime
from database.database import SessionLocal
from models import AIResponseORM

# Database Test Section

db = SessionLocal()

response1 = AIResponseORM(
    id="resp_001",
    text="Hello From SQLAlchemy",
    created_at=datetime.now()
)

response2 = AIResponseORM(
    id="resp_002",
    text="SQLAlchemy For AI Engineers",
    created_at=datetime.now()
)

response3 = AIResponseORM(
    id="resp_003",
    text="This should be rolled back",
    created_at=datetime.now()
)

db.add(response3)

response4 = AIResponseORM(
    id="resp_004",
    text="This should NOT survive",
    created_at=datetime.now()
)

db.add(response4)

response5 = AIResponseORM(
    id="resp_005",  # intentional duplicate
    text="This should also NOT survive",
    created_at=datetime.now()
)

db.add(response5)

response6 = AIResponseORM(
    id="resp_006",
    text="This is response six",
    created_at=datetime.now()
)

db.add(response4)

response7 = AIResponseORM(
    id="resp_007",  # intentional duplicate
    text="This is response seven",
    created_at=datetime.now()
)

db.add(response5)

db.commit()


