from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# DB Address
DATABASE_URL = "sqlite:///./cogentra.db"

# Engine responsible for communicating with the database
engine = create_engine(DATABASE_URL)

# Creates a sqlalchemy session for our app
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False
)

# Base class for all ORM models
Base = declarative_base()

