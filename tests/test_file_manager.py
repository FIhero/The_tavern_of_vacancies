import json

import pytest

from src.file_manager import JSONSaver
from src.vacancies import Vacancy


@pytest.fixture()
def temp_json_saver(tmp_path):
    # tmp_path - это фикстура pytest, которая предоставляет временную директорию
    file_path = tmp_path / "temp_vacancies.json"
    saver = JSONSaver(file_path)
    return saver


@pytest.fixture()
def sample_vacancy_objects():
    # Создаем несколько объектов Vacancy для использования в тестах
    v1 = Vacancy(
        "Мороженщик", "http://example.com/vac1", "Продавайте эксклюзив", 400, "Застрой"
    )
    v2 = Vacancy(
        "Кладоискатель",
        "http://example.com/vac2",
        "Ищите и всегда найдете",
        550000,
        "НЕпираты",
    )
    v3 = Vacancy(
        "Скрипач", "http://example.com/vac3", "Заскрипи соседей!", 20000, "МояЯгодка"
    )
    v4 = Vacancy(
        "Мишутка",
        "http://example.com/vac4",
        "За шугай соседей",
        2000,
        "Компания Медведав",
    )
    v3_duplicate_url = Vacancy(
        "Скрипач (дубликат)",
        "http://example.com/vac3",
        "Другое описание",
        20000,
        "МояЯгодка",
    )

    return [v1, v2, v3, v4, v3_duplicate_url]


def test_json_saver_add_initial_vacancies(temp_json_saver, sample_vacancy_objects):
    """Тестирует добавление нескольких вакансий и начальную запись в файл."""
    v1, v2, _, _, _ = sample_vacancy_objects

    temp_json_saver.add_vacancy(v1)
    temp_json_saver.add_vacancy(v2)

    assert temp_json_saver._filename.exists()
    with open(temp_json_saver._filename, "r", encoding="utf-8") as f:
        loaded_data = json.load(f)

    expected_data = [
        {
            "name": v1.name,
            "url": v1.url,
            "description": v1.description,
            "salary": v1.salary,
            "company_name": v1.company_name,
        },
        {
            "name": v2.name,
            "url": v2.url,
            "description": v2.description,
            "salary": v2.salary,
            "company_name": v2.company_name,
        },
    ]
    assert loaded_data == expected_data
    assert len(loaded_data) == 2


def test_json_saver_read_data(temp_json_saver, sample_vacancy_objects):
    """Тестирует чтение данных из файла."""
    v1, _, _, _, _ = sample_vacancy_objects

    initial_data_dict = {
        "name": v1.name,
        "url": v1.url,
        "description": v1.description,
        "salary": v1.salary,
        "company_name": v1.company_name,
    }

    with open(temp_json_saver._filename, "w", encoding="utf-8") as f:
        json.dump([initial_data_dict], f, ensure_ascii=False, indent=4)

    loaded_data = temp_json_saver._read_data()
    assert loaded_data == [initial_data_dict]


def test_json_saver_add_data_with_duplicates(temp_json_saver, sample_vacancy_objects):
    """Тестирует добавление новых данных к существующему файлу, включая дубликаты."""
    v3, v4, v3_duplicate_url = (
        sample_vacancy_objects[2],
        sample_vacancy_objects[3],
        sample_vacancy_objects[4],
    )

    temp_json_saver.add_vacancy(v3)
    temp_json_saver.add_vacancy(v4)
    temp_json_saver.add_vacancy(v3_duplicate_url)

    with open(temp_json_saver._filename, "r", encoding="utf-8") as f:
        loaded_data = json.load(f)

    expected_data = [
        {
            "name": v3.name,
            "url": v3.url,
            "description": v3.description,
            "salary": v3.salary,
            "company_name": v3.company_name,
        },
        {
            "name": v4.name,
            "url": v4.url,
            "description": v4.description,
            "salary": v4.salary,
            "company_name": v4.company_name,
        },
    ]
    assert loaded_data == expected_data
    assert len(loaded_data) == 2


def test_json_saver_delete_data(temp_json_saver, sample_vacancy_objects):
    """Тестирует удаление данных."""
    v1, v2, v3, _, _ = sample_vacancy_objects

    temp_json_saver.add_vacancy(v1)
    temp_json_saver.add_vacancy(v2)
    temp_json_saver.add_vacancy(v3)

    with open(temp_json_saver._filename, "r", encoding="utf-8") as f_before:
        assert len(json.load(f_before)) == 3

    delete_result = temp_json_saver.delete_vacancy(v1)
    assert delete_result is True

    with open(temp_json_saver._filename, "r", encoding="utf-8") as f_after:
        loaded_data = json.load(f_after)

    expected_data = [
        {
            "name": v2.name,
            "url": v2.url,
            "description": v2.description,
            "salary": v2.salary,
            "company_name": v2.company_name,
        },
        {
            "name": v3.name,
            "url": v3.url,
            "description": v3.description,
            "salary": v3.salary,
            "company_name": v3.company_name,
        },
    ]
    assert loaded_data == expected_data
    assert len(loaded_data) == 2

    non_existent_vacancy = Vacancy(
        "Несуществующая", "http://nonexistent.com", "asd", 100, "none"
    )
    delete_result_fail = temp_json_saver.delete_vacancy(non_existent_vacancy)
    assert delete_result_fail is False


def test_json_saver_get_vacancies(temp_json_saver, sample_vacancy_objects):
    """Тестирует получение и фильтрацию вакансий."""
    v1, v2, v3, _, _ = sample_vacancy_objects

    temp_json_saver.add_vacancy(v1)
    temp_json_saver.add_vacancy(v2)
    temp_json_saver.add_vacancy(v3)

    all_vacs = temp_json_saver.get_vacancies()
    assert len(all_vacs) == 3
    expected_all_vacs_dicts = [
        {
            "name": v1.name,
            "url": v1.url,
            "description": v1.description,
            "salary": v1.salary,
            "company_name": v1.company_name,
        },
        {
            "name": v2.name,
            "url": v2.url,
            "description": v2.description,
            "salary": v2.salary,
            "company_name": v2.company_name,
        },
        {
            "name": v3.name,
            "url": v3.url,
            "description": v3.description,
            "salary": v3.salary,
            "company_name": v3.company_name,
        },
    ]
    assert all_vacs == expected_all_vacs_dicts
    filtered_by_name = temp_json_saver.get_vacancies("мороженщик")
    assert len(filtered_by_name) == 1
    assert filtered_by_name[0]["name"] == "Мороженщик"
    filtered_by_desc = temp_json_saver.get_vacancies("ищите")
    assert len(filtered_by_desc) == 1
    assert filtered_by_desc[0]["name"] == "Кладоискатель"
    filtered_by_company = temp_json_saver.get_vacancies("МояЯгодка")
    assert len(filtered_by_company) == 1
    assert filtered_by_company[0]["name"] == "Скрипач"
    no_results = temp_json_saver.get_vacancies("выдумка")
    assert len(no_results) == 0
