import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 1. URL бази даних
# SQLALCHEMY_DATABASE_URL = "sqlite:///./queue_database.db"

# Беремо шлях з налаштувань Railway, а якщо його немає (на твоєму ПК) - беремо локальний
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./queue_database.db")

# 2. Engine (Двигун)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# 3. SessionLocal (Фабрика сесій)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовий клас для моделей (потрібен у models.py)
Base = declarative_base()

# --- ОСЬ ЦЬОГО ТОБІ НЕ ВИСТАЧАЛО ---
def get_db():
    """
    Функція-генератор для отримання сесії бази даних.
    FastAPI автоматично закриє сесію після виконання запиту.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()