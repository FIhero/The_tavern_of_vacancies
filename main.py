from src.api_handler import HeadHunterAPI
from src.file_manager import JSONSaver
from src.vacancies import Vacancy


def user_interaction():
    """Интерфейс для пользователя"""
    hh_api = HeadHunterAPI()
    json_saver = JSONSaver()
    greeting = (
        "Приветствуем вас на нашей платформе по поиску работы: 'Таверна вакансий'"
    )
    print(greeting)

    menu = [
        "1 - Найти вакансии",
        "2 - Показать сохраненные",
        "3 - Удалить вакансию",
        "4 - Выход",
    ]
    for item in menu:
        print(item)

    while True:
        command = input("\nВведите номер команды:")

        if command == "1":
            request = input("Введите ключевые слова для поиска:")
            print(f"Ищем по запросу {request}")
            hh_vacancies = hh_api.get_vacancies(request)
            if hh_vacancies and "items" in hh_vacancies and hh_vacancies["items"]:
                vac_obj = Vacancy.cast_to_object_list(hh_vacancies["items"])
                print(f"Нвйдено {len(vac_obj)} вакансий по запросу.")
                for item in vac_obj:
                    json_saver.add_vacancy(item)
                    print("Найденные вакансии были добавлены 'vacancies.json'")
                else:
                    print(f'По запросу "{request}" вакансий не найдено.')

        elif command == "2":
            saved_vac_dicts = json_saver.get_vacancies()
            if saved_vac_dicts:
                print("Загружаем сохраненные вакансии...")
                display_vac = Vacancy.cast_to_object_list(saved_vac_dicts)
                print(f"Всего сохранено {len(display_vac)} вакансий.")
                print("-" * 30)
                for i, vac in enumerate(display_vac):
                    salary_str = (
                        f"{vac.salary}" if vac.salary else "Зарплата не указана."
                    )
                    print(
                        f"{1 + i}. Название: {vac.name}\n"
                        f"Компания: {vac.company_name}\n"
                        f"Зарплата: {salary_str} RUB\n"
                        f"URL: {vac.url}\n"
                        f"Описание: {vac.description[:100]}"
                    )
                    print("-" * 30)
                else:
                    print("В файле 'vacancies.json' пока нет сохраненных вакансий")

        elif command == "3":
            saved_vac_dicts = json_saver.get_vacancies()
            if not saved_vac_dicts:
                print("Для удаления нет вакансий.")
                continue
            display_vac = Vacancy.cast_to_object_list(saved_vac_dicts)
            print("Список сохраненных вакансий:")
            for i, vac in enumerate(display_vac):
                print(f"{1 + i}. {vac.name} ({vac.company_name}) - {vac.url}\n")
                print("-" * 30)
                try:
                    chose = int(
                        input('Введите номер для удаления вакансий или "0" для отмены:')
                    )
                    if chose == 0:
                        print("Удаление отменено.")
                        continue
                    if 1 <= chose <= len(display_vac):
                        vac_delete = display_vac[chose - 1]
                        config = input(
                            f"Вы уверены что хотите удалить вакансию '{vac_delete.name}'? (да/нет):"
                        )
                        if config.lower() == "да":
                            if json_saver.delete_vacancy(vac_delete):
                                print(f"Вакансия '{vac_delete.name}' успешно удалена.")
                            else:
                                print(
                                    f"Не удалось удалить вакансию '{vac_delete.name}'"
                                )
                        else:
                            print("Неверный номер вакансии. Повторите попытку снова")

                except ValueError:
                    print("Некорректный ввод. Пожалуйста введите число")

        elif command == "4":
            print("Спасибо за использование нашей платформы! \nДо свидания")
            break

        else:
            print("Такого запроса не существует")


if __name__ == "__main__":
    user_interaction()
