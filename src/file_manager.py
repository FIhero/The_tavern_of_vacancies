import json
from abc import ABC, abstractmethod
from typing import List, Optional


class BaseFileSaver(ABC):
    @abstractmethod
    def add_vacancy(self, vacancy):
        """Добавление вакансии"""
        pass

    @abstractmethod
    def get_vacancies(self, criteria=None):
        """Фильтрация вакансий по критериям"""
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy):
        """Удаление вакансии от работодателя"""
        pass


class JSONSaver(BaseFileSaver):
    def __init__(self, filename: str = "vacancies.json"):
        self._filename = filename

    def _read_data(self) -> List[dict]:
        """Открывает JSON-файл и читает его"""
        data = []
        try:
            with open(self._filename, "r", encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            pass

        except json.JSONDecodeError:
            pass
        return data

    def _write_data(self, data: list[dict]):
        """Переписывает JSON-файл"""
        with open(self._filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def add_vacancy(self, vacancy):
        """Добавление вакансии в базу, с проверкой на дубликат"""
        data = self._read_data()
        vacancy_dict = {
            "name": vacancy.name,
            "url": vacancy.url,
            "description": vacancy.description,
            "salary": vacancy.salary,
            "company_name": vacancy.company_name,
        }

        for ev in data:
            if ev.get("url") == vacancy_dict.get("url"):
                print(f"Вакансия '{vacancy_dict.get('name')}' уже существует")
                break
        else:
            data.append(vacancy_dict)
            self._write_data(data)
            print(f"Вакансия '{vacancy_dict.get('name')}' успешно добавлена.")

    def get_vacancies(self, criteria: Optional[str] = None) -> List[dict]:
        """Фильтрация поиска по критериям"""
        data = self._read_data()

        if criteria:
            filtered_vacancy = []
            search_query = criteria.lower()

            for vacancy_dict in data:
                name = search_query in vacancy_dict.get("name", "").lower()
                description = (
                    search_query in vacancy_dict.get("description", "").lower()
                )
                company = search_query in vacancy_dict.get("company_name", "").lower()

                if name or description or company:
                    filtered_vacancy.append(vacancy_dict)

            return filtered_vacancy
        else:
            return data

    def delete_vacancy(self, vacancy):
        """Удаление из базы вакансий"""
        data = self._read_data()
        initial_count = len(data)

        update_data = [v for v in data if v.get("url") != vacancy.url]

        if len(update_data) < initial_count:
            self._write_data(update_data)
            return True
        else:
            return False
