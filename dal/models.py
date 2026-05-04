from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Enum
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime
import enum

from dal.database import Base


class EntryStatus(enum.Enum):
    WAITING = "waiting"
    PROCESSED = "processed"
    CANCELLED = "cancelled"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    # --- Нові атрибути, які ти просив ---
    full_name = Column(String, nullable=True)  # Прізвище та ім'я
    age = Column(Integer, nullable=True)  # Вік
    gender = Column(String, nullable=True)  # Стать
    bio = Column(String, nullable=True)  # Коротка інформація про себе

    # Зв'язки (Relationships)
    owned_queues = relationship("Queue", back_populates="owner")
    entries = relationship("QueueEntry", back_populates="user")


class Queue(Base):
    __tablename__ = "queues"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    is_open = Column(Boolean, default=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    # Зв'язки
    owner = relationship("User", back_populates="owned_queues")
    participants = relationship("QueueEntry", back_populates="queue", cascade="all, delete-orphan")


class QueueEntry(Base):
    __tablename__ = "queue_entries"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    queue_id = Column(Integer, ForeignKey("queues.id"))

    # Поле для сортування (хто перший став)
    joined_at = Column(DateTime, default=datetime.utcnow)
    status = Column(Enum(EntryStatus), default=EntryStatus.WAITING)

    # Зв'язки
    user = relationship("User", back_populates="entries")
    queue = relationship("Queue", back_populates="participants")