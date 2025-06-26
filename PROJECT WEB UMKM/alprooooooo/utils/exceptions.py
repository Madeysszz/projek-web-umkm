# utils/exceptions.py

class DatabaseConnectionError(Exception):
    pass

class DataNotFoundError(Exception):
    pass

class InvalidInputError(Exception):
    pass

class EmptyStackException(Exception):
    pass