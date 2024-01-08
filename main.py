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
    result = None
    @classmethod
    def __repr__(self):
        return self.__class__.__name__

    @classmethod
    def get_vacancies(self):
     text = input("Выберите профессию: ")
     per_page = int(input("Введите желаемое количество результатов вакансии: "))
     url = "https://api.hh.ru/vacancies"
     params = {
            "text": text,
            "areas": 113,
            "per_page" : per_page
     }
     response = requests.get(url, params=params)
     user_vacancies = {}
     if response.status_code == 200:
          data = response.json()
          vacancies  = {i: data[i] for i in ["items"]}
          with open("hh.json", 'w', encoding="utf-8") as file:
              json.dump(data, file, ensure_ascii=False, indent=4)
          if per_page is not None:
              counter = 0
              while True:
                for vacancy in vacancies["items"]:
                         if counter < per_page:
                            counter += 1
                            vacancy_id = vacancy.get("id")
                            vacancy_title = vacancy.get("name")
                            vacancy_url = vacancy.get("alternate_url")
                            vacancy_experience = vacancy.get("experience", {}).get("name")
                            company_name = vacancy.get("employer", {}).get("name")
                            vacancy_salary = vacancy.get("salary")
                            vacancy_description = "Нету описания"
                            if vacancy.get("salary") is not None:
                                if vacancy.get("salary", {}).get("currency") is not None:
                                    vacancy_currency = vacancy.get("salary", {}).get("currency")
                                else:
                                    vacancy_currency = ""
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

                            items = f'"ID": {vacancy_id},"Должность": {vacancy_title},"Ссылка": {vacancy_url},"Компания" :{company_name},"Зарплата": {vacancy_salary},"Валюта": {vacancy_currency},"Описание": {vacancy_description},"Опыт": {vacancy_experience}'
                            user_vacancies[items] = self.result


                else:
                    break
          return user_vacancies
     else:
        print(f"Request failed with status code: {response.status_code}")


class SuperJobAPI(Api):
    """Класс для работы с API сайта Super Job"""
    result = None
    @classmethod
    def __repr__(self):
        return self.__class__.__name__

    @classmethod
    def get_vacancies(self):
        text = input("Выберите профессию: ")
        count = int(input("Введите желаемое количество результатов вакансии: "))

        url = "https://api.superjob.ru/2.0/vacancies/"
        params = {
            "text": text,
            "count": count
        }
        headers = {
            "X-Api-App-Id": os.getenv("superjobapi")
        }
        response = requests.get(url,headers=headers, params=params)
        user_vacancies = {}
        if response.status_code == 200:
            data = response.json()
            vacancies = {i: data[i] for i in ["objects"]}
            with open("sj.json", 'w', encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
            if count is not None:
               counter = 0
               while True:
                for vacancy in vacancies["objects"]:
                    if counter < count:
                        counter += 1
                        vacancy_id = vacancy.get("id")
                        vacancy_title = vacancy.get("profession")
                        vacancy_url = vacancy.get("client", {}).get("link")
                        vacancy_experience = vacancy.get("experience", {}).get("title")
                        company_name = vacancy.get("client", {}).get("title")
                        vacancy_currency = vacancy.get("currency")
                        vacancy_description = "Нету описания"
                        if vacancy.get("payment_from") or vacancy.get("payment_to") == 0:
                            vacancy_salary = "Нету информации о зарплате"
                        else:
                            vacancy_salary = f'Зарплата от {vacancy.get("payment_from")} до {vacancy.get("payment_to")}'

                        if vacancy.get("client", {}).get("description") != "":
                            vacancy_description = vacancy.get("client", {}).get("description")
                        else:
                            vacancy_description = "Нету описания"

                        items = f'"ID": {vacancy_id},"Должность": {vacancy_title},"Ссылка": {vacancy_url},"Компания" :{company_name},"Зарплата": {vacancy_salary},"Валюта": {vacancy_currency},"Описание": {vacancy_description},"Опыт": {vacancy_experience}'
                        user_vacancies[items]=self.result
                else:
                    break
            return user_vacancies
        else:
            print(f"Request failed with status code: {response.status_code}")


class Vacancies:
    """Класс для работы с вакансиями"""
    def __init__(self):
        pass
    def validate(self):
        if not isinstance(self.vacancy_salary, (int, float)):
            raise ValueError("Зарплата должна быть в числах")

        if not isinstance(self.vacancy_title,str):
            raise ValueError("Название должно быть корректным")
    def sorted_vacancies(self):
        sorted_vacancies = []
        platform_input = int(
            input("С каких платформ вы хотите получить вакансии? Выберите 1 для hh.ru или 2 для superjob.ru) "))
        filter_words = input("Если вы хотите поискать по ключевому слову в вакансии,напишите это слово: ")
        if platform_input == 1:
         vacancies = HeadHunterAPI.get_vacancies()
         for vac in vacancies:
            if filter_words in vac:
                sorted_vacancies.append(f'"ID": {vacancy_id},"Должность": {vacancy_title},"Ссылка": {vacancy_url},"Компания" :{company_name},"Зарплата": {vacancy_salary},"Валюта": {vacancy_currency},"Описание": {vacancy_description},"Опыт": {vacancy_experience}')
                return sorted_vacancies
            else:
                return "Нет вакансий, соответствующих заданным критериям."

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
    def delete_vacancy(self,criteria):
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
        pass

def user_interaction():
    print("Добро пожаловать в платформу поиска вакансий")
    user_choice = int(input("Если вы хотите просмотреть вакансии по выбранной профессии нажмите 1,"
                            "а если хотите просмотреть вакансии по ключевому слову нажмите 2 "))
    if user_choice == 1:
        platform_input = int(input("С каких платформ вы хотите получить вакансии? Выберите 1 для hh.ru или 2 для superjob.ru) "))
        if platform_input == 1:
            vacancies = HeadHunterAPI.get_vacancies()
            json_file = JSONSaver("new.json")
            json_file.add_vacancy(vacancies)
            with open("new.json", "r") as file:
                jsonData = json.load(file)
                print(jsonData)
        elif platform_input == 2:
            vacancies = SuperJobAPI.get_vacancies()
            json_file = JSONSaver("new.json")
            json_file.add_vacancy(vacancies)
            with open("new.json", "r") as file:
                jsonData = json.load(file)
                print(jsonData)
        else :
            input("Введите 1 или 2")

    elif user_choice == 2:
        vacancy = Vacancies()
        vacancy.sorted_vacancies()




if __name__ == "__main__":
    user_interaction()


# hh_api = HeadHunterAPI()
# hh_vacancies = hh_api.get_vacancies()
# print(hh_vacancies)
# superjob_api = SuperJobAPI()
# superjob_vacancies = superjob_api.get_vacancies()
# print(superjob_vacancies)
#
# vacancy = Vacancies()
# vacancy.sorted_vacancies()
