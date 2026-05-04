from sqlalchemy.orm import Session
from sqlalchemy import func
from .models import User, Queue, QueueEntry, EntryStatus

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, username: str, hashed_password: str,
               full_name: str = None, age: int = None,
               gender: str = None, bio: str = None) -> User:
        """Створюємо юзера з новими додатковими атрибутами"""
        db_user = User(
            username=username,
            hashed_password=hashed_password,
            full_name=full_name,
            age=age,
            gender=gender,
            bio=bio
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def get_by_id(self, user_id: int) -> User:
        return self.db.query(User).filter(User.id == user_id).first()

    def get_by_username(self, username: str) -> User:
        return self.db.query(User).filter(User.username == username).first()


class QueueRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, name: str, owner_id: int) -> Queue:
        # У нас вже було поле name, тому тут просто підтверджуємо стабільність
        db_queue = Queue(name=name, owner_id=owner_id)
        self.db.add(db_queue)
        self.db.commit()
        self.db.refresh(db_queue)
        return db_queue

    def get_all(self):
        return self.db.query(Queue).all()

    def get_by_id(self, queue_id: int) -> Queue:
        return self.db.query(Queue).filter(Queue.id == queue_id).first()

    def update_status(self, queue_id: int, is_open: bool) -> Queue:
        db_queue = self.get_by_id(queue_id)
        if db_queue:
            db_queue.is_open = is_open
            self.db.commit()
            self.db.refresh(db_queue)
        return db_queue


class QueueEntryRepository:
    def __init__(self, db: Session):
        self.db = db

    def add_to_queue(self, user_id: int, queue_id: int) -> QueueEntry:
        entry = QueueEntry(user_id=user_id, queue_id=queue_id)
        self.db.add(entry)
        self.db.commit()
        self.db.refresh(entry)
        return entry

    def get_entry(self, queue_id: int, user_id: int) -> QueueEntry:
        return self.db.query(QueueEntry).filter(
            QueueEntry.queue_id == queue_id,
            QueueEntry.user_id == user_id
        ).first()

    def get_first_waiting(self, queue_id: int) -> QueueEntry:
        return self.db.query(QueueEntry).filter(
            QueueEntry.queue_id == queue_id,
            QueueEntry.status == EntryStatus.WAITING
        ).order_by(QueueEntry.joined_at.asc()).first()

    def delete_entry(self, entry: QueueEntry):
        self.db.delete(entry)
        self.db.commit()

    def get_position(self, queue_id: int, user_id: int) -> int:
        user_entry = self.get_entry(queue_id, user_id)
        if not user_entry:
            return 0

        count = self.db.query(func.count(QueueEntry.id)).filter(
            QueueEntry.queue_id == queue_id,
            QueueEntry.status == EntryStatus.WAITING,
            QueueEntry.joined_at < user_entry.joined_at
        ).scalar()

        return count + 1