from passlib.context import CryptContext
from dal.repositories import UserRepository, QueueRepository, QueueEntryRepository
from dal.models import User, Queue, QueueEntry
from .exceptions import (
    QueueNotFoundException,
    QueueClosedException,
    AlreadyInQueueException,
    UserNotFoundException,
    NotAnOwnerException,
    QueueEmptyException
)

# Налаштування безпеки
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


class AuthService:
    """Сервіс для безпеки (тільки технічні функції)"""

    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)


class QueueService:
    """Головний сервіс, що об'єднує роботу з юзерами та чергами"""

    def __init__(
            self,
            u_repo: UserRepository,
            q_repo: QueueRepository,
            qe_repo: QueueEntryRepository
    ):
        self.u_repo = u_repo
        self.q_repo = q_repo
        self.qe_repo = qe_repo

    # --- Сценарії КОРИСТУВАЧА ---

    def register_user(self, username: str, password: str,
                      full_name: str = None, age: int = None,
                      gender: str = None, bio: str = None):
        """Реєстрація нового користувача з усіма атрибутами"""

        if self.u_repo.get_by_username(username):
            raise Exception(f"Користувач з іменем {username} вже існує")

        # 1. Відрізаємо пробіли по краях (.strip())
        # 2. Жорстко обрізаємо до 72 символів ([:72]), щоб bcrypt ніколи не падав
        safe_password = password.strip()[:72]

        # Хешуємо вже безпечний пароль
        hashed_pw = AuthService.hash_password(safe_password)

        return self.u_repo.create(
            username=username,
            hashed_password=hashed_pw,
            full_name=full_name,
            age=age,
            gender=gender,
            bio=bio
        )

    def create_queue(self, name: str, owner_id: int):
        """Створення черги (користувач стає хазяїном)"""
        return self.q_repo.create(name=name, owner_id=owner_id)

    def join_queue(self, queue_id: int, user_id: int):
        """Заняття місця у черзі"""
        queue = self.q_repo.get_by_id(queue_id)

        if not queue:
            raise QueueNotFoundException(f"Чергу {queue_id} не знайдено")

        if not queue.is_open:
            raise QueueClosedException("Ця черга закрита для запису")

        # Чи не стоїть він там вже?
        existing = self.qe_repo.get_entry(queue_id, user_id)
        if existing:
            raise AlreadyInQueueException("Ви вже є у цій черзі")

        return self.qe_repo.add_to_queue(user_id, queue_id)

    def get_my_position(self, queue_id: int, user_id: int):
        """Перегляд місця в черзі"""
        pos = self.qe_repo.get_position(queue_id, user_id)
        if pos == 0:
            raise UserNotFoundException("Вас немає в цій черзі")
        return pos

    # --- Сценарії ХАЗЯЇНА ---

    def call_next(self, queue_id: int, requester_id: int):
        """Команда «наступний» (FIFO)"""
        queue = self.q_repo.get_by_id(queue_id)

        if not queue:
            raise QueueNotFoundException("Чергу не знайдено")

        if queue.owner_id != requester_id:
            raise NotAnOwnerException("Ви не маєте прав керування цією чергою")

        first_entry = self.qe_repo.get_first_waiting(queue_id)
        if not first_entry:
            raise QueueEmptyException("Черга порожня")

        self.qe_repo.delete_entry(first_entry)
        return True

    def remove_user_from_queue(self, queue_id: int, user_to_remove_id: int, requester_id: int):
        """Видалити заданого користувача"""
        queue = self.q_repo.get_by_id(queue_id)

        if queue.owner_id != requester_id:
            raise NotAnOwnerException("Доступ заборонено")

        entry = self.qe_repo.get_entry(queue_id, user_to_remove_id)
        if not entry:
            raise UserNotFoundException("Користувача не знайдено в черзі")

        self.qe_repo.delete_entry(entry)

    def close_registration(self, queue_id: int, requester_id: int):
        """Закрити можливість запису"""
        queue = self.q_repo.get_by_id(queue_id)

        if not queue:
            raise QueueNotFoundException("Чергу не знайдено")

        if queue.owner_id != requester_id:
            raise NotAnOwnerException("Дія доступна тільки хазяїну")

        return self.q_repo.update_status(queue_id, is_open=False)