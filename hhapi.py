from api import Api
import requests
import json


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

