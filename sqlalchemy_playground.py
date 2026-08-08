from datetime import datetime
from database.database import SessionLocal
from models import AIResponseORM

# Database Test Section
db = SessionLocal()

# Python objects (Table Entries)
play1 = AIResponseORM(
    id="play_001",
    text="Hello From SQLAlchemy",
    created_at=datetime.now()
)

play2 = AIResponseORM(
    id="play_002",
    text="SQLAlchemy For AI Engineers",
    created_at=datetime.now()
)

play3 = AIResponseORM(
    id="play_003",
    text="This should be rolled back",
    created_at=datetime.now()
)

play4 = AIResponseORM(
    id="play_004",
    text="This should NOT survive",
    created_at=datetime.now()
)

play5 = AIResponseORM(
    id="play_005",
    text="This should also NOT survive",
    created_at=datetime.now()
)

play6 = AIResponseORM(
    id="play_006",
    text="This is response six",
    created_at=datetime.now()
)

play7 = AIResponseORM(
    id="play_007",
    text="This is response seven",
    created_at=datetime.now()
)

play8 = AIResponseORM(
    id="play_008",
    text="This is response seven",
    created_at=datetime.now()
)

play9 = AIResponseORM(
    id="play_009",
    text="This is response seven",
    created_at=datetime.now()
)

play10 = AIResponseORM(
    id="play_010",
    text="This is response seven",
    created_at=datetime.now()
)

play11 = AIResponseORM(
    id="play_011",
    text="This is response seven",
    created_at=datetime.now()
)

play12 = AIResponseORM(
    id="play_012",
    text="This is response seven",
    created_at=datetime.now()
)

play13 = AIResponseORM(
    id="play_013",
    text="This is response seven",
    created_at=datetime.now()
)
# db.add(play13)

# Commits changes to the database
db.commit()