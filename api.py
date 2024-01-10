from abc import ABC, abstractmethod

class Api(ABC):
    """Абстрактный класс для работы с API сайтов с вакансиями"""
    @abstractmethod
    def __repr__(self):
        pass

