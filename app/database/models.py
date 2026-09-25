from datetime import datetime, timezone

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Float,
    Text,
    ForeignKey
)

from app.database.connection import Base


class User(Base):

    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        String,
        unique=True,
        index=True,
        nullable=False
    )

    password_hash = Column(
        String,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc)
    )


class Trip(Base):

    __tablename__ = "trips"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        String,
        ForeignKey("users.user_id"),
        nullable=False,
        index=True
    )

    thread_id = Column(
        String,
        nullable=False,
        index=True
    )

    destination = Column(
        String,
        nullable=True
    )

    duration_days = Column(
        Integer,
        nullable=True
    )

    transport = Column(
        String,
        nullable=True
    )

    total_budget = Column(
        Float,
        nullable=True
    )

    itinerary = Column(
        Text,
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc)
    )