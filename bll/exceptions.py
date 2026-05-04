class QueueBaseException(Exception):
    """Базовий клас для всіх помилок нашої системи"""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

# Помилки доступу (Хазяїн vs Користувач)
class NotAnOwnerException(QueueBaseException):
    """Виникає, коли не-хазяїн намагається керувати чергою"""
    pass

class AccessDeniedException(QueueBaseException):
    """Загальна помилка доступу"""
    pass

# Помилки стану черги
class QueueNotFoundException(QueueBaseException):
    """Чергу не знайдено в базі"""
    pass

class QueueClosedException(QueueBaseException):
    """Спроба записатися в закриту чергу"""
    pass

class QueueEmptyException(QueueBaseException):
    """Спроба викликати 'наступного', коли черга порожня"""
    pass

# Помилки користувача
class AlreadyInQueueException(QueueBaseException):
    """Користувач вже стоїть у цій черзі"""
    pass

class UserNotFoundException(QueueBaseException):
    """Користувача не знайдено"""
    pass