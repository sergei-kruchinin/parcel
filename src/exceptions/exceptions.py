"""
Модуль exceptions.exceptions

Содержит классы исключений для обработки в сервисах

"""
class ParcelNotFoundError(Exception):
    pass

class ParcelDatabaseError(Exception):
    pass

class ParcelValidationError(Exception):
    pass