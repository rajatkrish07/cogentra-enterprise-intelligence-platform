from __future__ import annotations
from datetime import datetime
from sqlalchemy import DateTime, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.database import Base, engine

# User ORM Model
class UserORM(Base):
    __tablename__ = "user_orm"
    id: Mapped[str] = mapped_column(
        String,
        primary_key=True
    )
    username: Mapped[str] = mapped_column(
        String,
        nullable=False,
        unique=True
    )
    email: Mapped[str] = mapped_column(
        String,
        nullable=False,
        unique=True
    )
    chats: Mapped[list[ChatORM]] = relationship()

    first_name: Mapped[str] = mapped_column(
        String,
        nullable=False
    )
    last_name: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

# Chat ORM Model
class ChatORM(Base):
    __tablename__ = "chats_orm"

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "title",
            name = "uq_chat_user_title"
        ),
    )

    id: Mapped[str] = mapped_column(
        String,
        primary_key=True
    )
    user_id: Mapped[str] = mapped_column(
        ForeignKey("user_orm.id"),
        nullable=False
    )
    title: Mapped[str] = mapped_column(
        String,
        nullable=False
    )
    messages: Mapped[list[MessageORM]] = relationship()

# Message ORM Model
class MessageORM(Base):
    __tablename__ = "messages_orm"
    id: Mapped[str] = mapped_column(
        String,
        primary_key=True
    )
    chat_id: Mapped[str] = mapped_column(
        ForeignKey("chats_orm.id"),
        nullable=False,
    )
    timestamp: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )
    text: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )
    responses: Mapped[list[AIResponseORM]] = relationship()

# AIResponse ORM Model
class AIResponseORM(Base):
    __tablename__ = "ai_response_orm"
    id: Mapped[str] = mapped_column(
        String,
        primary_key=True
    )
    message_id: Mapped[str] = mapped_column(
        ForeignKey("messages_orm.id"),
        nullable=False
    )
    text: Mapped[str] = mapped_column(
        String,
        nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

