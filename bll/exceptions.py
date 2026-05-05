class QueueBaseException(Exception):
   
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class NotAnOwnerException(QueueBaseException):
    
    pass

class AccessDeniedException(QueueBaseException):
  
    pass

class QueueNotFoundException(QueueBaseException):
   
    pass

class QueueClosedException(QueueBaseException):
    
    pass

class QueueEmptyException(QueueBaseException):
    
    pass

class AlreadyInQueueException(QueueBaseException):
    
    pass

class UserNotFoundException(QueueBaseException):
  
    pass
