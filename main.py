from jsonfile import JSONSaver
from vacancies import Vacancies
from hhapi import HeadHunterAPI
from sjapi import SuperJobAPI
import json



def user_interaction():
    """Функция для взаимодействия с пользователем. Пользователь может самостоятельно выбрать платформу,
    количество отображаемых вакансий и может искать вакансии по ключевому слову
    """
    print("Добро пожаловать в платформу поиска вакансий")
    user_choice = int(input("Если вы хотите просмотреть вакансии по выбранной профессии нажмите 1,"
                            "а если хотите просмотреть вакансии по ключевому слову нажмите 2 "))
    if user_choice == 1:
        platform_input = int(input("С каких платформ вы хотите получить вакансии? Выберите 1 для hh.ru или 2 для superjob.ru) "))
        if platform_input == 1:
            vacancies = HeadHunterAPI.get_vacancies()
            json_file = JSONSaver("hh.json")
            json_file.add_vacancy(vacancies)
            with open("hh.json", "r") as file:
                jsonData = json.load(file)
            print("Создан новый файл с вакансиями")
            print(jsonData)
            new_choice = int(input(
                "Если вы хотите удалить результаты поиска,то нажмите 1,если хотите продолжить поиск вакансий,нажмите 2, если хотите выйти,нажмите 3"))
            if new_choice == 1:
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
            json_file = JSONSaver("sj.json")
            json_file.add_vacancy(vacancies)
            with open("sj.json", "r") as file:
                jsonData = json.load(file)
            print("Создан новый файл с вакансиями")
            print(jsonData)
            new_choice = int(input(
                "Если вы хотите удалить результаты поиска,то нажмите 1,если хотите продолжить поиск вакансий,нажмите 2, если хотите выйти,нажмите 3"))
            if new_choice == 1:
                json_file.delete_vacancy(vacancies)
                print("Файл с вакансиями успешно удалён")
            elif new_choice == 2:
                return
            elif new_choice == 3:
                quit()
            else:
                print("Выберите один из предоставленных вариантов")

        else:
            input("Введите 1 или 2")

    elif user_choice == 2:
        vacancy = Vacancies()
        vacancy.sorted_vacancies()
        print("Создан новый файл с вакансиями")






if __name__ == "__main__":
    user_interaction()

