import requests
import os
from abc import ABC, abstractmethod
import json


class Api(ABC):
    """Абстрактный класс для работы с API сайтов с вакансиями"""
    @abstractmethod
    def __repr__(self):
        pass


class HeadHunterAPI(Api):
    """Класс для работы с API сайта Head Hunter"""
    @classmethod
    def __repr__(self):
        return self.__class__.__name__

    @classmethod
    def get_vacancies(self):

        url = "https://api.hh.ru/vacancies"
        params = {
            "text": input("Выберите профессию: "),
            "areas": 113,
            "per_page": input("Введите желаемое количество результатов вакансии: ")
        }
        response = requests.get(url, params=params)
        user_vacancies = []
        while len(user_vacancies) != "per_page":
          if response.status_code == 200:
            data = response.json()
            vacancies = data.get("items")
            for vacancy in vacancies:
                vacancy_id = vacancy.get("id")
                vacancy_title = vacancy.get("name")
                vacancy_url = vacancy.get("alternate_url")
                vacancy_experience = vacancy.get("experience", {}).get("name")
                company_name = vacancy.get("employer", {}).get("name")
                vacancy_salary = vacancy.get("salary")
                if vacancy.get("salary", {}).get("currency") is not None:
                    vacancy_currency = vacancy.get("salary", {}).get("currency")
                else :
                    vacancy_currency =  ""
                if vacancy_salary is not None:
                    vacancy_salary_from = vacancy.get("salary", {}).get("from")
                    vacancy_salary_to = vacancy.get("salary", {}).get("to")
                    vacancy_salary = f"От {vacancy_salary_from} до {vacancy_salary_to}"
                    vacancy_currency = vacancy.get("salary", {}).get("currency")
                else:
                    vacancy_salary = "Нету информации о зарплате"

                if vacancy.get("address") is not None:
                    if vacancy.get("address", {}).get("description") is not None:
                        vacancy_description = vacancy.get("address", {}).get("description")
                    else:
                        vacancy_description = "Нету описания"

                data = {"ID": vacancy_id,"Должность": vacancy_title,"Компания": company_name,"Ссылка": vacancy_url,"Зарплата": vacancy_salary,"Валюта": vacancy_currency,"Описание": vacancy_description,"Опыт": vacancy_experience}
                user_vacancies.append(data)
            return user_vacancies
          else:
            print(f"Request failed with status code: {response.status_code}")

class SuperJobAPI(Api):
    """Класс для работы с API сайта Super Job"""
    @classmethod
    def __repr__(self):
        return self.__class__.__name__

    @classmethod
    def get_vacancies(self):

        url = "https://api.superjob.ru/2.0/vacancies/"
        params = {
            "text": input("Выберите профессию: "),
            "count": input("Введите желаемое количество результатов вакансии: ")
        }
        headers = {
            "X-Api-App-Id": os.getenv("superjobapi")
        }
        response = requests.get(url,headers=headers, params=params)
        user_vacancies = []
        while len(user_vacancies) != "per_page":
         if response.status_code == 200:
            data = response.json()
            vacancies = data.get("objects")
            with open("sj.json", 'w', encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
            for vacancy in vacancies:
                vacancy_id = vacancy.get("id")
                vacancy_title = vacancy.get("profession")
                vacancy_url = vacancy.get("client", {}).get("link")
                vacancy_experience = vacancy.get("experience", {}).get("title")
                company_name = vacancy.get("client", {}).get("title")
                vacancy_currency = vacancy.get("currency")
                if vacancy.get("payment_from") or vacancy.get("payment_to") == 0:
                    vacancy_salary = "Нету информации о зарплате"
                else:
                    vacancy_salary = f'Зарплата от {vacancy.get("payment_from")} до {vacancy.get("payment_to")}'

                if vacancy.get("client", {}).get("description") == "" :
                    vacancy_description = "Нету описания"
                else:
                    vacancy_description = vacancy.get("client", {}).get("description")

                data = {"ID": vacancy_id,"Должность": vacancy_title,"Компания": company_name,"Ссылка": vacancy_url,"Зарплата": vacancy_salary,"Валюта": vacancy_currency,"Описание": vacancy_description,"Опыт": vacancy_experience}
                user_vacancies.append(data)
            return user_vacancies
         else:
                print(f"Request failed with status code: {response.status_code}")


class Vacancies:
    """Класс для работы с вакансиями"""
    def __init__(self,title,url,experience,company_name,salary,description):
        self.title = title
        self.url = url
        self.experience = experience
        self.company_name = company_name
        self.salary = salary
        self.description = description


    def compare_salaries(self,other):
        if self.salary > other.salary:
            return f"У {self.title} зарпалат выше чем {other.salary}"
        elif other.salary > self.salary:
            return f"У {other.title} зарпалат выше чем {self.salary}"
        else:
            return f"Зарплаты у {self.title} и {other.salary} равны"
#Класс должен поддерживать методы сравнения вакансий между собой по зарплате и валидировать данные,
# которыми инициализируются его атрибуты. ???

class JSONDATA(ABC):
    """Абстрактный класс, который обязывает реализовать методы для добавления вакансий в файл"""
    @abstractmethod
    def __repr__(self):
        pass

    @abstractmethod
    def add_vacancy(self,*args):
        pass

    @abstractmethod
    def get_vacancies_by_salary(self,*args):
        pass

    @abstractmethod
    def delete_vacancy(self):
        pass

class JSONSaver(JSONDATA):
    """Класс для сохранения информации о вакансиях в JSON-файл"""
    def __init__(self):
        self.vacancies = f"{input('Название файла с вакансиями: ')}.json"

    def __repr__(self):
        return self.vacancies

    def add_vacancy(self, vacancy):
        with open(self.vacancies, 'w', encoding="utf-8") as file:
            json.dump(vacancy, file, ensure_ascii=False, indent=4)

    def get_vacancies_by_salary(self, salary):
        with open(self.vacancies, 'r', encoding="utf-8") as file:
            pass
    #Как он должен выбрать по зарплате?


    def delete_vacancy(self):
        path = os.path.join(self.vacancies)
        os.remove(path)

#
# hh_api = HeadHunterAPI()
# hh_vacancies = hh_api.get_vacancies()
superjob_api = SuperJobAPI()
superjob_vacancies = superjob_api.get_vacancies()
print(superjob_vacancies)
# new_vacancy = Vacancies("title","url","experience","company","100 000-150 000 руб","big company")
# json_saver = JSONSaver()
# json_saver.add_vacancy(new_vacancy)
#json_saver.get_vacancies_by_salary("100 000-150 000 руб")


