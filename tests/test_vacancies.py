import pytest

from src.vacancies import Vacancy


@pytest.fixture()
def vacancy_info():
    vac1 = Vacancy(
        "Продавец-касир",
        "http//pochet.com",
        "Не пыльная работа (подпись на рабство)",
        50000,
        "К&Ь",
    )
    vac2 = Vacancy(
        "Горничная (только мужчины)",
        "http//pornhab.com",
        "Берем исключительно мужчин!",
        {"from": 350000.0, "to": 450000.0},
        "PohabGod",
    )

    vac4 = Vacancy(
        "Горничная (только мужчины)",
        "http//pornhab.com",
        "Берем исключительно мужчин!",
        {"from": 350000.0},
        "PohabGod",
    )

    vac5 = Vacancy(
        "Горничная (только мужчины)",
        "http//pornhab.com",
        "Берем исключительно мужчин!",
        {"to": 450000.0},
        "PohabGod",
    )

    vac3 = Vacancy("", "", "", 0, "")

    vacancy = [vac1, vac2, vac3, vac4, vac5]
    return vacancy


@pytest.fixture()
def hh_api_raw_data_fixture():
    """Фикстура, имитирующая сырые данные, возвращаемые HeadHunterAPI.get_vacancies()."""
    mock_data = {
        "items": [
            {
                "id": "93353083",
                "premium": False,
                "name": "Тестировщик комфорта квартир",
                "department": None,
                "has_test": False,
                "response_letter_required": False,
                "area": {
                    "id": "26",
                    "name": "Воронеж",
                    "url": "https://api.hh.ru/areas/26",
                },
                "salary": {
                    "from": 350000,
                    "to": 450000,
                    "currency": "RUR",
                    "gross": False,
                },
                "type": {"id": "open", "name": "Открытая"},
                "address": None,
                "response_url": None,
                "sort_point_distance": None,
                "published_at": "2024-02-16T14:58:28+0300",
                "created_at": "2024-02-16T14:58:28+0300",
                "archived": False,
                "apply_alternate_url": "https://hh.ru/applicant/vacancy_response?vacancyId=93353083",
                "branding": {"type": "CONSTRUCTOR", "tariff": "BASIC"},
                "show_logo_in_search": True,
                "insider_interview": None,
                "url": "https://api.hh.ru/vacancies/93353083?host=hh.ru",
                "alternate_url": "https://hh.ru/vacancy/93353083",
                "relations": [],
                "employer": {
                    "id": "3499705",
                    "name": "Специализированный застройщик BM GROUP",
                    "url": "https://api.hh.ru/employers/3499705",
                    "alternate_url": "https://hh.ru/employer/3499705",
                    "logo_urls": {
                        "original": "https://hhcdn.ru/employer-logo-original/1214854.png",
                        "240": "https://hhcdn.ru/employer-logo/6479866.png",
                        "90": "https://hhcdn.ru/employer-logo/6479865.png",
                    },
                    "vacancies_url": "https://api.hh.ru/vacancies?employer_id=3499705",
                    "accredited_it_employer": False,
                    "trusted": True,
                },
                "snippet": {
                    "requirement": "Занимать активную жизненную позицию, уметь активно танцевать и громко петь. "
                                   "Обладать навыками коммуникации, чтобы налаживать добрососедские отношения. "
                                   "Обладать системным мышлением...",
                    "responsibility": "Оценивать вид из окна: встречать рассветы на кухне, и провожать алые "
                                      "закаты в спальне. Оценивать инфраструктуру района: ежедневно ходить на...",
                },
                "contacts": None,
                "schedule": {"id": "flexible", "name": "Гибкий график"},
                "working_days": [],
                "working_time_intervals": [],
                "working_time_modes": [],
                "accept_temporary": False,
                "professional_roles": [{"id": "107", "name": "Руководитель проектов"}],
                "accept_incomplete_resumes": False,
                "experience": {"id": "noExperience", "name": "Нет опыта"},
                "employment": {"id": "full", "name": "Полная занятость"},
                "adv_response_url": None,
                "is_adv_vacancy": False,
                "adv_context": None,
            },
            {},
        ],
        "found": 2,
        "pages": 1,
        "per_page": 20,
        "page": 0,
    }
    return mock_data


def test_addendum_vacancy(vacancy_info):
    """Тест добавления вакансии"""
    v, _, _, _, _ = vacancy_info
    assert v.name == "Продавец-касир"
    assert v.url == "http//pochet.com"
    assert v.description == "Не пыльная работа (подпись на рабство)"
    assert v.salary == 50000
    assert v.company_name == "К&Ь"


def test_from_to_vacancy(vacancy_info):
    """Тестирует, что дает при валидации цен"""
    _, v, _, v1, v2 = vacancy_info
    assert v.name == "Горничная (только мужчины)"
    assert v.url == "http//pornhab.com"
    assert v.description == "Берем исключительно мужчин!"
    assert v.salary == 400000.0
    assert v.company_name == "PohabGod"
    assert v1.salary == 350000.0
    assert v2.salary == 450000.0


def test_empty_vacancy(vacancy_info):
    """Тестирует реакцию на пустую вакансию"""
    _, _, v, _, _ = vacancy_info
    assert v.name == ""
    assert v.url == ""
    assert v.description == ""
    assert v.salary == 0.0
    assert v.company_name == ""


def test_cast_to_object_list(hh_api_raw_data_fixture):
    """Тестирование статического метода Vacancy.cast_to_object_list."""
    vacancies_objects = Vacancy.cast_to_object_list(hh_api_raw_data_fixture["items"])

    assert isinstance(vacancies_objects, list)
    assert len(vacancies_objects) == 2

    vac1 = vacancies_objects[0]
    assert isinstance(vac1, Vacancy)
    assert vac1.name == "Тестировщик комфорта квартир"
    assert vac1.url == "https://hh.ru/vacancy/93353083"
    assert vac1.salary == 400000.0
    assert vac1.company_name == "Специализированный застройщик BM GROUP"
    assert "Занимать активную жизненную позицию" in vac1.description
    assert "Оценивать вид из окна" in vac1.description

    vac2 = vacancies_objects[1]
    assert isinstance(vac2, Vacancy)
    assert vac2.name == "Не указано"
    assert vac2.url == ""
    assert vac2.salary == 0.0
    assert vac2.company_name == "Неизвестно"
    assert vac2.description == "Нет описания"


def test_for_lt(vacancy_info):
    """Тестирует функцию lt в классе Vacancy"""
    v1, v2, v3, _, _ = vacancy_info

    assert v1 < v2
    assert v3 < v1
    assert v3 < v2


def test_type_error_for_lt():
    """Тестирует ошибку в функции __lt__ класса Vacancy"""
    obj = ("траляля", "тополя")
    test_vac = Vacancy("name", "url", "desc", 1000, "company")
    with pytest.raises(
        TypeError, match="Можно использовать только объекты класса Vacancy"
    ):
        test_vac < obj


def test_for_eq(vacancy_info):
    """Тестирует функцию __eq__ класса Vacancy"""
    v1, v2, _, _, _ = vacancy_info
    v3 = Vacancy(
        "Продавец-касир",
        "http//pochet.com",
        "Не пыльная работа (подпись на рабство)",
        50000,
        "К&Ь",
    )
    assert v1 == v3
    assert v2 != v3


def test_type_error_for_eq():
    """Тестирует ошибку в функции __eq__ класса Vacancy"""
    obj = ("траля ля", "тополя")
    v3 = Vacancy(
        "Продавец-касир",
        "http//pochet.com",
        "Не пыльная работа (подпись на рабство)",
        50000,
        "К&Ь",
    )
    assert Vacancy.__eq__(v3, obj) is False
