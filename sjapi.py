from api import Api
import requests
import json
import os


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
