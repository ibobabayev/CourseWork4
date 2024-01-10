from hhapi import HeadHunterAPI
from sjapi import SuperJobAPI
from jsonfile import JSONSaver

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
        filter_words = input("Напишите слово,которое хотите поискать в вакансиях: ")
        if platform_input == 1:
           vacancies = HeadHunterAPI.get_vacancies()
           for vac in vacancies:
                if filter_words in vac:
                    sorted_vacancies.append(f'"ID": {vacancy_id},"Должность": {vacancy_title},"Ссылка": {vacancy_url},"Компания" :{company_name},"Зарплата": {vacancy_salary},"Валюта": {vacancy_currency},"Описание": {vacancy_description},"Опыт": {vacancy_experience}')
                    print("Создан новый файл с вакансиями")
                    return sorted_vacancies
                else:
                    return "Нет вакансий, соответствующих заданным критериям."
           new_choice = int(input(
               "Если вы хотите удалить результаты поиска,то нажмите 1,если хотите продолжить поиск вакансий,нажмите 2, если хотите выйти,нажмите 3"))
           if new_choice == 1:
               json_file = JSONSaver("hh.json")
               json_file.add_vacancy(vacancies)
               json_file.delete_vacancy(vacancies)
               print("Файл с вакансиями успешно удалён")
           elif new_choice == 2:
               return
           elif new_choice == 3:
               quit()
           else:
               print("Выберите один из предоставленных вариантов")
        elif platform_input == 2:
             vacancies = SuperJobAPI.get_vacancies()
             for vac in vacancies:
                 if filter_words in vac:
                     sorted_vacancies.append(f'"ID": {vacancy_id},"Должность": {vacancy_title},"Ссылка": {vacancy_url},"Компания" :{company_name},"Зарплата": {vacancy_salary},"Валюта": {vacancy_currency},"Описание": {vacancy_description},"Опыт": {vacancy_experience}')
                     print("Создан новый файл с вакансиями")
                     return sorted_vacancies
                 else:
                    return "Нет вакансий, соответствующих заданным критериям."
             new_choice = int(input(
                 "Если вы хотите удалить результаты поиска,то нажмите 1,если хотите продолжить поиск вакансий,нажмите 2, если хотите выйти,нажмите 3"))
             if new_choice == 1:
                 json_file = JSONSaver("sj.json")
                 json_file.add_vacancy(vacancies)
                 json_file.delete_vacancy(vacancies)
                 print("Файл с вакансиями успешно удалён")
             elif new_choice == 2:
                 return
             elif new_choice == 3:
                 quit()
             else:
                 print("Выберите один из предоставленных вариантов")