from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import List, Optional


# --- СХЕМИ КОРИСТУВАЧА ---

class UserBase(BaseModel):
    """Базові поля, які є всюди"""
    username: str
    full_name: Optional[str] = None
    age: Optional[int] = Field(None, ge=0, le=120)  # Валідація: вік від 0 до 120
    gender: Optional[str] = None


class UserCreate(UserBase):
    """Те, що приходить від клієнта при реєстрації"""
    password: str


class UserResponse(UserBase):
    """Те, що ми віддаємо клієнту (без пароля)"""
    id: int
    bio: Optional[str] = None

    # Дозволяє Pydantic читати дані прямо з об'єктів SQLAlchemy
    model_config = ConfigDict(from_attributes=True)


# --- СХЕМИ ЗАПИСУ В ЧЕРЗІ ---

class QueueEntryResponse(BaseModel):
    """Інформація про місце конкретного юзера в черзі"""
    id: int
    user_id: int
    queue_id: int
    joined_at: datetime
    # Вкладаємо схему юзера, щоб бачити не просто ID, а ім'я того, хто стоїть
    user: UserResponse

    model_config = ConfigDict(from_attributes=True)


# --- СХЕМИ ЧЕРГИ ---

class QueueBase(BaseModel):
    """Базові поля черги"""
    name: str


class QueueCreate(QueueBase):
    """Дані для створення нової черги"""
    owner_id: int


class QueueResponse(QueueBase):
    """Повна інформація про чергу для показу на сайті"""
    id: int
    is_open: bool
    owner_id: int
    # Список учасників: за замовчуванням порожній список
    participants: List[QueueEntryResponse] = []

    model_config = ConfigDict(from_attributes=True)