from api import ABC,abstractmethod
import json

class JSONDATA(ABC):
    """Абстрактный класс, который обязывает реализовать методы для добавления вакансий в файл"""
    @abstractmethod
    def __repr__(self):
        pass

    @abstractmethod
    def add_vacancy(self,vacancy):
        pass

    @abstractmethod
    def get_vacancy(self,criteria):
        pass

    @abstractmethod
    def delete_vacancy(self,vacancy):
        pass


class JSONSaver(JSONDATA):
    """Класс для сохранения информации о вакансиях в JSON-файл"""
    def __init__(self,file):
        self.file = file

    def __repr__(self):
        return self.file

    def add_vacancy(self, vacancy):
        with open(self.file, "w", encoding="utf-8") as file:
            json.dump(vacancy, file, ensure_ascii=False, indent=4)
            file.write("\n")


    def get_vacancy(self, criteria):
        result = []
        with open(self.file, "r", encoding="utf-8") as file:
            for line in file:
                vacancy_data = json.loads(line)
                if criteria in vacancy_data.values():
                    result.append(vacancy_data)
        print(result)

    def delete_vacancy(self, vacancy):
        with open(self.file, 'w') as file:
            file.write('')
