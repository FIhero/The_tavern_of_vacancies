from typing import Optional, Union


class Vacancy:
    __slots__ = ("name", "url", "description", "salary", "company_name")

    def __init__(
        self,
        name: str,
        url: str,
        description: str,
        salary: Optional[float],
        company_name: str,
    ):
        self.name = name
        self.url = url
        self.description = description
        self.salary = self._validate_salary(salary)
        self.company_name = company_name

    def _validate_salary(
        self, raw_salary: Union[float, int, dict[str, float], None]
    ) -> float:
        """Метод для валидации и обработки зп"""
        if raw_salary is None:
            return 0.0
        elif isinstance(raw_salary, (int, float)):
            return float(raw_salary)
        elif isinstance(raw_salary, dict):
            s_from = raw_salary.get("from")
            s_to = raw_salary.get("to")
            if s_from is not None and s_to is not None:
                calculate = float((s_from + s_to) / 2)
                return round(calculate, 2)
            elif s_from is not None:
                calculate = float(s_from)
                return round(calculate, 2)
            elif s_to is not None:
                calculate = float(s_to)
                return round(calculate, 2)
        return 0.0

    @staticmethod
    def cast_to_object_list(raw_vacancy_data: list) -> list:
        """Преобразование информации из JSON-файла в вакансию"""
        vac_object_list = []
        for i, item_data in enumerate(raw_vacancy_data):
            try:
                name = item_data.get("name", "Не указано")
                url = item_data.get("alternate_url", "")
                snippet = item_data.get("snippet", {})
                description_text = []
                if "requirement" in snippet and snippet["requirement"]:
                    description_text.append(snippet["requirement"])
                if "responsibility" in snippet and snippet["responsibility"]:
                    description_text.append(snippet["responsibility"])
                description = (
                    ". ".join(description_text) if description_text else "Нет описания"
                )
                salary_data = item_data.get("salary")
                company_info = item_data.get("employer", {})
                company_name = company_info.get("name", "Неизвестно")
                vac_obj = Vacancy(
                    name=name,
                    url=url,
                    description=description,
                    salary=salary_data,
                    company_name=company_name,
                )

                vac_object_list.append(vac_obj)

            except Exception as e:
                print(f"Произошла непредвиденная ошибка при обработке элемента {e}")
        return vac_object_list

    def __lt__(self, other):
        """Сравнение вакансий по зарплате (self < other)"""
        if not isinstance(other, Vacancy):
            raise TypeError("Можно использовать только объекты класса Vacancy")
        return self.salary < other.salary

    def __eq__(self, other):
        """Проверка идентичности вакансий по имени, url, компании и зарплате"""
        if not isinstance(other, Vacancy):
            return False
        return (
            self.salary == other.salary
            and self.name == other.name
            and self.company_name == other.company_name
            and self.url == other.url
        )
